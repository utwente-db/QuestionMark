
def aer_matcher(blocks_file):
    blocks = []
    with open(blocks_file) as file:
        for block in file:
            if block == '[]\n':
                continue
            else:
                print(block)
                block = block.strip('\n').strip('][').split(', ')
                print(block)
                print(type(block))
                block = list(map(int, block))
                blocks.append(block)
    print(blocks)


if __name__ == '__main__':
    # # #  Incrementally Adaptive Sorted Neighborhood blocking
    aer_matcher('datasets/asn_gs_blocks')  # normal execution.
