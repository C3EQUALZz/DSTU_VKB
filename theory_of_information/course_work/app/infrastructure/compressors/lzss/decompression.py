"""
Implementation of the LZSS decompression algorithm.
"""

from app.infrastructure.compressors import utils
from app.infrastructure.compressors.lzss.configuration import Configuration


class Decompressor:
    """
    The implementation of the decompressor.
    """

    configuration = None
    """
    The configuration class to use.

    :type: :class:`class`
    """

    def __init__(self, configuration=Configuration):
        """
        :param configuration: The configuration class to use.
        :type configuration: class
        """
        self.configuration = configuration

    def decompress(self, source):
        """
        Decompress the given source buffer using the LZSS algorithm.

        :param source: The source buffer to decompress.
        :type source: bytearray

        :return: The uncompressed data.
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

        # Prepare an empty ring buffer of size `RING_BUFFER_SIZE`, with extra
        # `MATCH_LENGTH_MAX - 1` bytes to facilitate string comparison.
        text_buffer = bytearray(
            self.configuration.RING_BUFFER_SIZE
            + self.configuration.MATCH_LENGTH_MAX
            - 1
        )

        # Determine the current end position inside the ring buffer.
        text_buffer_end = (
                self.configuration.RING_BUFFER_SIZE - self.configuration.MATCH_LENGTH_MAX
        )

        # Clear the ring buffer by setting the corresponding entries to a whitespace
        # character. This has to be used in conjunction with the encoding procedure.
        # According to the original author, any character which occurs often is possible
        # here.
        for index in range(text_buffer_end):
            text_buffer[index] = ord(" ")

        # Initialize the mask value to 0.
        flags = 0

        # Unlike in the original implementation, we are using a variable to count the
        # mask position. The original approach - which depends on a unsigned integer
        # variable for the flags variable - does not seem to work directly. In fact the
        # counter approach should be more readable.
        # We initialize this to 7 to indicate that a new flags byte has to be read in
        # the first step.
        flags_used_bits_count = 7

        # Handle all the input.
        while True:
            # Shift the flags/mask to the next position.
            flags >>= 1

            # We have just consumed another bit of the flags/mask value.
            flags_used_bits_count += 1

            if flags_used_bits_count == 8:
                # If we have reached the last element of the bit mask, save the bit mask
                # and reset it.

                # Reset the counter.
                flags_used_bits_count = 0

                # Stop if we have reached the end of the input.
                if source_position == source_length:
                    break

                # Retrieve the new flags/mask value from the input and move one position
                # forward.
                flags = source[source_position]
                source_position += 1

            # Handle the current instruction.
            if flags & 1:
                # This is a literal instruction.

                # Stop if we have reached the end of the input.
                if source_position == source_length:
                    break

                # Retrieve the current byte from the input.
                current_byte = source[source_position]
                source_position += 1

                # Add the current byte to the output directly.
                destination.append(current_byte)
                destination_position += 1

                # Add the current byte at the end of the ring buffer.
                text_buffer[text_buffer_end] = current_byte

                # Move to the next entry of the ring buffer.
                text_buffer_end += 1
                text_buffer_end &= self.configuration.RING_BUFFER_SIZE - 1
            else:
                # This is a match instruction.

                # Stop if we have reached the end of the input.
                if source_position == source_length:
                    break

                # Retrieve the first byte from the input.
                # This corresponds to the first byte of the match position.
                first_byte = source[source_position]
                source_position += 1

                # Stop if we have reached the end of the input.
                if source_position == source_length:
                    break

                # Retrieve the second byte from the input.
                # This corresponds to the second part of the match position and the
                # match length.
                second_byte = source[source_position]
                source_position += 1

                # Determine the match position inside the ring buffer.
                # The match position has 12 bits. The first byte of the input holds the
                # least significant byte of the position, while the second byte of the
                # input holds the 4 most significant bits of the position.
                match_position = first_byte | ((second_byte & 0xF0) << 4)

                # Determine the match length.
                # The match length has 4 bits. It is stored in the last 4 bits of the
                # second byte.
                # We have to apply the minimum length threshold to correct the value.
                # Additionally we have to add a value of 1 as a length of 0 does not
                # make any sense for a match instruction.
                match_length = utils.get_last_bits(second_byte, 4)
                match_length += self.configuration.MATCH_LENGTH_MIN_THRESHOLD
                match_length += 1

                # Copy the data byte by byte.
                for offset_index in range(match_length):
                    # Determine the current index inside the ring buffer.
                    buffer_index = (match_position + offset_index) & (
                            self.configuration.RING_BUFFER_SIZE - 1
                    )

                    # Retrieve the current byte from the ring buffer.
                    current_byte = text_buffer[buffer_index]

                    # Add the current byte to the output.
                    destination.append(current_byte)
                    destination_position += 1

                    # Add the current byte at the end of the ring buffer.
                    text_buffer[text_buffer_end] = current_byte

                    # Move to the next entry of the ring buffer.
                    text_buffer_end += 1
                    text_buffer_end &= self.configuration.RING_BUFFER_SIZE - 1

        # Return the destination buffer.
        return destination
