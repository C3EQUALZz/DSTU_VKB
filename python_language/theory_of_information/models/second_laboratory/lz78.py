class LZ78:

    def compress(self, text: str) -> list[tuple[int, str]]:
        """
        Compresses the input text using LZ78 algorithm.

        :param text: Input text to compress.
        :return: List of tuples where each tuple is (index, char).
        """
        compressed = []
        dictionary = {}
        current_string = ""

        for char in text:
            current_string += char
            if current_string not in dictionary:
                index = len(dictionary) + 1
                dictionary[current_string] = index
                compressed.append((dictionary.get(current_string[:-1], 0), char))
                current_string = ""

        return compressed

    def decompress(self, compressed: list[tuple[int, str]]) -> str:
        """
        Decompresses the list of tuples back to the original text using LZ78 algorithm.

        :param compressed: List of tuples where each tuple is (index, char).
        :return: Decompressed text.
        """
        dictionary = {}
        decoded_string = ""

        for index, char in compressed:
            if index == 0:
                decoded_string += char
            else:
                prefix = dictionary.get(index, "")
                decoded_string += prefix + char
            # Update the dictionary with the new entry
            dictionary[len(dictionary) + 1] = decoded_string

        return decoded_string
