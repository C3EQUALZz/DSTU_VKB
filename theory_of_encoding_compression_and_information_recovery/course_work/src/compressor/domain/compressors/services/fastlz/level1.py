"""
Implementation of the FastLZ compression algorithm, level 1.
"""

from compressor.domain.compressors.errors import BadDataError
from compressor.domain.compressors.services.fastlz.common import (
    calculate_hash_value,
    compare_buffer_content_until_mismatch,
    emit_literal_instructions,
    memcpy,
    memmove,
    read_unsigned_integer_32_bit,
)
from compressor.domain.compressors.services.fastlz.configuration import FastLZConfiguration
from compressor.domain.compressors.services.fastlz.utils import get_last_bits


class Compressor:
    """
    The implementation of the (string) compressor for level 1.
    """

    def __init__(self, configuration: type[FastLZConfiguration] = FastLZConfiguration) -> None:
        """
        :param configuration: The configuration class to use.
        :type configuration: class
        """
        self.configuration: type[FastLZConfiguration] = configuration

    def compress(self, source: bytearray) -> bytearray:
        """
        Compress the given source buffer using the FastLZ algorithm.

        :param source: The source buffer to compress.
        :type source: bytearray

        :return: The compression result.
        :rtype: bytearray
        """
        # The source parameters: the current position inside the source buffer and the
        # overall length of the source buffer.
        source_position = 0
        source_length = len(source)

        # Due to using unaligned loads of unsigned 32 bit integers for the hash
        # hash calculation after determining the match length with our version of the
        # `flz_cmp` function, we have to keep the last 4 bytes untouched in `flz_cmp`.
        source_bound = source_length - 4

        # The position at which to call `flz_finalize`. With this our final literal
        # instruction will have (up to) 12 bytes. (We use the `- 1` as we are comparing
        # it using `>=`.)
        source_limit = source_length - 12 - 1

        # The destination buffer and the current position inside it (which corresponds
        # to the output length).
        destination = bytearray()
        destination_position = 0

        # Initialize the hash table using `0` for every possible entry. This is the same
        # as in the original, except that we do not explicitly use a loop here.
        hash_table = [0] * self.configuration.HASH_TABLE_SIZE

        # Initialize the current anchor point, id est the start position of the current
        # iteration.
        iteration_start_position = source_position

        # Move 2 bytes forward.
        # The minimum match length is 3, so these 2 bytes and the first byte being
        # ignored while hashing (see the first `current_sequence &= 0xFFFFFF` construct
        # below) are being skipped at the beginning. With this comparisons will avoid
        # detecting a match for the first 3 bytes with itself.
        source_position += 2

        # Iterate until the end of the input has been reached.
        while source_position < source_limit:
            # Find a match.
            while True:
                # Read the first 4 bytes of the current input and only keep the 3 least
                # significant ones.
                current_sequence = read_unsigned_integer_32_bit(source, source_position)
                current_sequence &= 0xFFFFFF

                # Hash the current group of 3 bytes.
                current_hash = calculate_hash_value(current_sequence, self.configuration)

                # Get the position of the referenced entry by retrieving the
                # corresponding index from the hash table.
                referenced_position = hash_table[current_hash]

                # Save the current position inside the hash table (this might replace
                # an existing value).
                hash_table[current_hash] = source_position

                # Determine the current offset between the input position and the
                # referenced position.
                current_offset = source_position - referenced_position

                # Retrieve the value at the referenced position.
                if current_offset < self.configuration.MATCH_OFFSET_MAX_LEVEL1:
                    # The offset is small enough, so we will keep the 3 least
                    # significant bytes of the value to compare it.
                    comparison_value = read_unsigned_integer_32_bit(source, referenced_position)
                    comparison_value &= 0xFFFFFF
                else:
                    # The offset is too large, so we will use (1 << 24) > (2^24 - 1),
                    # where (2^24 - 1) is the largest value being representable with 24
                    # bits (= 3 bytes).
                    comparison_value = 0x1000000

                # Stop if the position limit has been reached.
                if source_position >= source_limit:
                    break

                # Move to the next input position.
                source_position += 1

                # Stop if we have found a match with at least 3 bytes.
                if current_sequence == comparison_value:
                    break

            # Stop if the position limit has been reached.
            if source_position >= source_limit:
                break

            # Decrease the current position again as we have increased it in the last
            # step of the loop above, but there has been a match 1 byte before.
            source_position -= 1

            # Check whether the current position is after the start position of the
            # current iteration.
            # This is true for every match, which should hold in most of the cases.
            # If this is the case, emit the corresponding literal instructions.
            if source_position > iteration_start_position:
                # We still have to determine the literal length here.
                output_length = emit_literal_instructions(
                    source,
                    destination,
                    iteration_start_position,
                    source_position - iteration_start_position,
                    self.configuration,
                )
                destination_position += output_length

            # Determine the match length.
            # We increase the positions by 3 as we have already checked the first 3
            # bytes in the loop above.
            # This implies the minimal match length of 3 as well.
            match_length = compare_buffer_content_until_mismatch(
                source, referenced_position + 3, source_position + 3, source_bound
            )

            # Emit the corresponding match instructions.
            output_length = self._emit_match_instructions(destination, match_length, current_offset)
            destination_position += output_length

            # Move the input position to the end of match minus 2 bytes.
            source_position += match_length

            # Get the next 4 bytes.
            current_sequence = read_unsigned_integer_32_bit(source, source_position)

            # Save the current position for the hash of the 3 least significant bytes.
            current_hash = calculate_hash_value(current_sequence & 0xFFFFFF, self.configuration)
            hash_table[current_hash] = source_position
            source_position += 1

            # Save the current position for the hash of the 3 most significant bytes.
            current_sequence >>= 8
            current_hash = calculate_hash_value(current_sequence, self.configuration)
            hash_table[current_hash] = source_position
            source_position += 1

            # Save the new start value for the next iteration.
            iteration_start_position = source_position

        # Emit the final literal instruction.
        literal_length = source_length - iteration_start_position
        output_length = emit_literal_instructions(
            source,
            destination,
            iteration_start_position,
            literal_length,
            self.configuration,
        )
        destination_position += output_length

        # Return the destination buffer.
        return destination

    def _emit_match_instructions(self, destination: bytearray, match_length: int, match_offset: int) -> int:
        """
        Emit the given match instruction. If the match length exceeds
        `MATCH_LENGTH_MAX`, multiple match instructions will be emitted.

        :param destination: The destination buffer to write the instructions to.
        :type destination: bytearray

        :param match_length: The match length to emit.
        :type match_length: int

        :param match_offset: The match offset to emit.
        :type match_offset: int

        :return: The number of bytes written to the destination buffer.
        :rtype: int
        """
        # We have written nothing until now.
        bytes_written = 0

        # Reduce the offset by 1 as an offset of `0` does not make sense as this would
        # be the current byte itself.
        match_offset -= 1

        # Save the value for easier access.
        match_length_max = self.configuration.MATCH_LENGTH_MAX

        # Handle instruction of maximum match length.
        if match_length > (match_length_max - 2):
            # The match length to encode exceeds the maximum match length of an
            # instruction.
            # So emit match instructions and reduce it until the match length fits 1
            # additional instruction.
            # We use the `- 2` as a match length of 3 bytes gets the value 1 and this
            # is the difference.

            while match_length > (match_length_max - 2):
                # This will always be a long match instruction.

                # Write opcode[0].
                # (7 << 5) = 11100000_2 is the indicator for a long match.
                # `distance >> 8` fills the 5 least significant bits, corresponding to
                # the 5 most significant bits of the offset.
                to_write = (7 << 5) + (match_offset >> 8)
                destination.append(to_write)
                bytes_written += 1

                # Write opcode[1].
                # The match length is 264 - 2 - 7 - 2 = 253.
                # For the final `- 2`, see the explanation above as well.
                to_write = match_length_max - 2 - 7 - 2
                destination.append(to_write)
                bytes_written += 1

                # Write opcode[2].
                # This is the least significant byte of the offset.
                destination.append(match_offset & 255)
                bytes_written += 1

                # Reduce the match length by the one just emitted.
                match_length -= match_length_max - 2

        # Handle the last match instruction.
        if match_length < 7:  # noqa: PLR2004
            # This is a short match instruction.

            # Write opcode[0].
            # The 3 most significant bits will be the match length (range 3 to 8; value
            # 1 = 3-byte-match, value 2 = 4-byte-match ...)
            # The 5 least significant bits will be the 5 most significant bits of the
            # offset.
            to_write = (match_length << 5) + (match_offset >> 8)
            destination.append(to_write)
            bytes_written += 1

            # Write opcode[1].
            # This is the least significant byte of the offset.
            destination.append(match_offset & 255)
            bytes_written += 1
        else:
            # This is a long match instruction.

            # Write opcode[0].
            # (7 << 5) = 11100000_2 is the indicator for a long match.
            # `distance >> 8` fills the 5 least significant bits, corresponding to
            # the 5 most significant bits of the offset.
            to_write = (7 << 5) + (match_offset >> 8)
            destination.append(to_write)
            bytes_written += 1

            # Write opcode[1].
            # This is the match length.
            # We subtract `7` - corresponding to the long match indicator in the 3
            # most significant bits of opcode[0].
            destination.append(match_length - 7)
            bytes_written += 1

            # Write opcode[2].
            # This is the least significant byte of the offset.
            destination.append(match_offset & 255)
            bytes_written += 1

        # Return the number of bytes written.
        return bytes_written


class Decompressor:
    """
    The implementation of the (string) decompressor for level 1.
    """

    configuration = None
    """
    The configuration class to use.

    :type: :class:`class`
    """

    def __init__(self, configuration: type[FastLZConfiguration] = FastLZConfiguration) -> None:
        """
        :param configuration: The configuration class to use.
        :type configuration: class
        """
        self.configuration: type[FastLZConfiguration] = configuration

    def decompress(self, source: bytearray) -> bytearray:
        """
        Decompress the given source buffer using the FastLZ algorithm.

        :param source: The source buffer to decompress.
        :type source: bytearray

        :return: The decompression result.
        :rtype: bytearray
        """
        # The source parameters: the current position inside the source buffer and the
        # overall length of the source buffer.
        source_position = 0
        source_length = len(source)

        # The destination buffer and the current position inside it (which corresponds
        # to the output length).
        destination = bytearray()
        destination_position = 0

        # Get the first instruction code.
        # We only need the last 5 bits of the current byte to decide which type of
        # instruction we have.
        # As in the original implementation, we are not checking if the first
        # instruction really is a literal instruction. To detect this, we would have to
        # save the full byte to check if the 3 most significant bits actually are `000`.
        instruction_code = get_last_bits(source[source_position], bits=5)
        source_position += 1

        # Iterate until the end of the input has been reached.
        while source_position < source_length:
            # Handle the different instruction types.
            if instruction_code >= 32:  # noqa: PLR2004
                # This is a match instruction.
                # This cannot be reached in the first iteration, as there are only 5
                # bits (with a maximum value of 11111_2 = 31) - the first instruction
                # should be a literal instruction anyway, as we have nothing to copy for
                # the match.
                # Starting with the second iteration, `instruction_code` will always be
                # one byte not starting with `000` (the identifier for a literal
                # instruction) in the match instruction case, so we will always have at
                # least 00100000_2 = 32.

                # Retrieve the length value from opcode[0], using the 3 most
                # significant bits of it.
                # We can subtract one, as the smallest length value for a 3-byte-match
                # uses the value 1.
                match_length = (instruction_code >> 5) - 1

                # Retrieve the 5 most significant bits of the offset from opcode[0].
                # Afterwards we shift the current offset value to get an empty byte at
                # the end for the least significant byte of the offset.
                match_offset_part1 = get_last_bits(instruction_code, bits=5) << 8

                # We can already calculate the position of the copy operation here.
                # This is possible as we are already working with the shifted offset
                # value here.
                # The `-1` basically means `offset + 1`, as an offset of 0 does not
                # make much sense. We could write destination_position - (match_offset_part1 + 1)
                # as well to make it more obvious, but without the brackets it may
                # actually be faster.
                referenced_index = destination_position - match_offset_part1 - 1

                # Handle long match instructions.
                if match_length == (7 - 1):
                    # This is a long match instruction.
                    # A long match is indicated by 111_2 = 7, but we are using
                    # `match_length - 1` for the comparison here (see the retrieval of
                    # the match length from the input above), so we have to compare with
                    # 7 - 1 = 6.

                    # Make sure that we can read another byte.
                    if source_position >= source_length:
                        msg = "End of input reached too early."
                        raise BadDataError(msg)

                    # The length is set in opcode[1], which we retrieve here.
                    # Add this to 6, as this is the difference between the minimum match
                    # length of short and long match instructions.
                    match_length += source[source_position]
                    source_position += 1

                # The second (short match) or third (long match) byte holds the 8 least
                # significant bits of the offset, so retrieve it, correct the match
                # position and move the input forward.
                referenced_index -= source[source_position]
                source_position += 1

                # Increase the match length by 3, which is the minimum match length for
                # short instructions.
                match_length += 3

                # Abort if the referenced position is before the start of the
                # destination buffer.
                # Please note that this could cause errors if used with a dictionary
                # shared across the different blocks, but as we are starting with an
                # empty dictionary on every block compression run, this is no problem
                # for us.
                if referenced_index < 0:
                    msg = "Referenced index is too small."
                    raise BadDataError(msg)

                # Copy the specified amount of bytes. We have to use `memmove` as there
                # might be overlaps.
                memmove(destination, referenced_index, match_length)
                destination_position += match_length
            else:
                # This is a literal instruction.
                # This will always be the first instruction - for this reason
                # `instruction_code = source[0] & 31` (or any of its equivalents) is
                # allowed before the loop above, as the identifier `000` at the
                # beginning of the byte can be ignored (000X_2 = X_2).

                # Add 1 to the length value, as a value of 0 indicates a literal length
                # of 1 (a literal length of 0 does not make any sense at all).
                literal_length = instruction_code + 1

                # Make sure that we have enough bytes left in the input.
                if source_position + literal_length > source_length:
                    msg = "Not enough values available to copy with literal instruction."
                    raise BadDataError(msg)

                # Copy the specified amount of bytes. We can use `memcpy` as there are
                # no overlaps.
                memcpy(source, destination, source_position, literal_length)

                # Move the positions forward.
                source_position += literal_length
                destination_position += literal_length

            # Stop if the end of the input has been reached to be able to read the next
            # byte.
            if source_position >= source_length:
                break

            # Get the next instruction code.
            # Unlike in the first iteration (the value being assigned before the loop),
            # we now need the full byte as copy operations make sense now.
            instruction_code = source[source_position]
            source_position += 1

        # Return the destination buffer.
        return destination
