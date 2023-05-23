import random


class channel:
    def __init__(self, bits_list):
        self.input_bits = bits_list.copy()
        self.output_bits = bits_list.copy()
        self.error_ratio = 0
        self.errors = 0
        self.length = len(bits_list)

    def random_errors(self, error_ratio):

        for i in range(0, int(self.length * error_ratio)):  # generating x mistakes in random places
            rand_location = random.randint(0, self.length - 1)
            self.output_bits[rand_location] = (self.output_bits[rand_location] + 1) % 2  # zamiana na przeciwny bit

        self.errors = int(self.length * error_ratio)
        self.error_ratio = error_ratio

    def group_errors(self, size_of_group, space_between_groups):
        i = 0
        temp_errors = 0
        while (i + size_of_group) < self.length:

            for j in range(0, size_of_group):
                self.output_bits[i + j] = (self.output_bits[i + j] + 1) % 2  # changing to opposite value
                j += j
                temp_errors = temp_errors + 1

            i = i + j + space_between_groups - 1  # skipping next x bits
            j = 0
        self.errors = temp_errors
        self.error_ratio = temp_errors / self.length  # TODO: zaokraglanie do ?

    def group_noise(self, size_of_group, space_between_groups):
        i = 0
        temp_errors = 0
        while (i + size_of_group) < self.length:
            noise_value = random.randint(0, 1)  # picking randomly whether the group noise will be all zeros or all ones
            for j in range(0, size_of_group):
                self.output_bits[i + j] = noise_value
                j += j
                temp_errors = temp_errors + 1

            i = i + j + space_between_groups - 1  # skipping next x bits
            j = 0
            self.errors = temp_errors
            self.error_ratio = temp_errors / self.length

            # p = GOOD->BAD

    # q = BAD->GOOD

    def gilbert_elliot_model(self, p, q):
        new_bits = []
        temp_errors = 0
        state = 'G'  # Initial state: good channel

        for bit in self.output_bits:
            if state == 'G':  # Good channel state
                if random.random() > q:
                    new_bits.append(1 - bit)  # Flip the bit
                    state = 'B'  # Transition to bad channel state
                    temp_errors += 1

                else:
                    new_bits.append(bit)

            elif state == 'B':  # Bad channel state
                if random.random() < p:
                    new_bits.append(1 - bit)  # Flip the bit
                    state = 'G'  # Transition to good channel state
                    temp_errors += 1

                else:
                    new_bits.append(bit)

        self.output_bits = new_bits
        self.errors = temp_errors
        self.error_ratio = temp_errors / self.length

    def send(self, data):
        return data
