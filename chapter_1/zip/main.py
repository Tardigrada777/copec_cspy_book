# класс, представляющий сжатый ген
# изначально ген представлен строкой типа "A" или "С и проч.
# мы можем представить его последовательностью битов
class CompressedGene:
    def __init__(self, gene: str):
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        self.bit_string: int = 1 # начальная метка
        for nucleotide in gene.upper():
            # сдвигаем метку на два бита влево
            # таким образом справа появляются 00
            self.bit_string <<= 2 

            # если нуклеотид А, то последние 00 меняем на 00 и так далее
            # оператор | - логическое ИЛИ, выберет любое значение отличное от нуля
            if nucleotide == 'A':
                self.bit_string |= 0b00
            elif nucleotide == 'C':
                self.bit_string |= 0b01
            elif nucleotide == 'G':
                self.bit_string |= 0b10
            elif nucleotide == 'T':
                self.bit_string |= 0b11
            else:
                raise ValueError('Invalid Nucleotide:{}'.format(nucleotide))

    def decompress(self) -> str:
        gene: str = ''
        for i in range(0, self.bit_string.bit_length() - 1, 2):
            bits: int = self.bit_string >> i & 0b11
            if bits == 0b00: #A
                gene += 'A'
            elif bits == 0b01: #C
                gene += 'C'
            elif bits == 0b10: #G
                gene += 'G'
            elif bits == 0b11: #T
                gene += 'T'
            else:
                raise ValueError('Invalid Nucleotide:{}'.format(gebe))
        return gene[::-1]

    def __str__(self) -> str:
        return self.decompress()


if __name__ == '__main__':
    from sys import getsizeof
    original: str = 'TAGATACACTAGCCGATCGACCGACGTAGATACACTAGCCGATCGACCGACGTAGATACACTAGCCGATCGACCGACGTAGATACACTAGCCGATCGACCGACG' * 100
    print('original is {} bytes'.format(getsizeof(original)))
    compressed = CompressedGene(original)
    print('compressed is {} bytes'.format(getsizeof(compressed.bit_string)))
    print('original and compressed are the same?: {}'.format(original == compressed.decompress()))
    percent = (getsizeof(compressed.bit_string) / getsizeof(original))*100
    print('compression ratio is: {}%'.format(100 - percent))