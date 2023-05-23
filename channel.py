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
            self.error_ratio = temp_errors / self.length  # TODO: zaokraglanie do ?

    # p1 - probability of the channel being in the good state
    # p2 - probability of error in the bad or transition state
    # pg - probability of error in the good state
    # pb - probability of error in the bad or transition state

    def gilbert_elliot_model(self, p1, p2, pg, pb):
        state = 1  # initialize to good state
        received_bits = []
        temp_errors = 0
        for bit in self.output_bits:
            # determine the probability of staying in the current state or transitioning to the other state
            if state == 1:  # good state
                p = p1
                q = 1 - p1
            else:  # bad/transition state
                p = p2
                q = 1 - p2

            # update the state based on a Markov chain with memory
            if random.random() < p and bit == 0:  # stay in good state and no error
                state = 1
                received_bits.append(bit)
            elif random.random() < q and bit == 0:  # transition to bad/transition state and no error
                state = 0
                received_bits.append(bit)
            elif random.random() < pg and bit == 1:  # stay in bad/transition state and good bit error
                state = 0
                received_bits.append(0)
                temp_errors += 1
            elif random.random() < pb and bit == 1:  # transition to good state and bad/transition bit error
                state = 1
                received_bits.append(0)
                temp_errors += 1
            elif random.random() < pg and bit == 0:  # stay in bad/transition state and good bit error
                state = 0
                received_bits.append(1)
                temp_errors += 1
            elif random.random() < pb and bit == 0:  # transition to good state and bad/transition bit error
                state = 1
                received_bits.append(1)
                temp_errors += 1
            else:  # stay in current state and no error
                received_bits.append(bit)

        self.output_bits = received_bits
        self.errors = temp_errors
        self.error_ratio = temp_errors / self.length
    def send(self, data):
        return data
