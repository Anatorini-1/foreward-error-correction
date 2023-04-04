import random


class channel:
    def __init__(self, bits_list):
        self.bits = bits_list

    def random_error(self, amount_of_errors):
        for i in range(0, amount_of_errors):  # generating x mistakes in random places
            rand_location = random.randint(0, len(self.bits) - 1)
            self.bits[rand_location] = (self.bits[rand_location] + 1) % 2
        return self.bits

    def group_errors(self, size_of_group, space_between_groups):
        i = 0
        while (i + size_of_group) < (len(self.bits)):

            for j in range(0, size_of_group):
                # print(i + j, '\n')
                self.bits[i + j] = (self.bits[i + j] + 1) % 2  # changing to opposite value
                j += j

            i = i + j + space_between_groups  # skipping next x bits
            j = 0
            print(i, '\n')
        return self.bits

    def group_noise(self, size_of_group, space_between_groups):
        i = 0
        while (i + size_of_group) < (len(self.bits)):
            noise_value = random.randint(0, 1)  # picking randomly whether the group noise will be all zeros or all ones
            for j in range(0, size_of_group):
                # print(i + j, '\n')
                self.bits[i + j] = noise_value
                j += j

            i = i + j + space_between_groups  # skipping next x bits
            j = 0
            print(i, '\n')
        return self.bits

    # p1 - probability of the channel being in the good state
    # p2 - probability of error in the bad or transition state
    # pg - probability of error in the good state
    # pb - probability of error in the bad or transition state
    def gilbert_elliot_model(self, p1, p2, pg, pb):
        state = 1  # initialize to good state
        received_bits = []
        for bit in self.bits:
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
            elif random.random() < pb and bit == 1:  # transition to good state and bad/transition bit error
                state = 1
                received_bits.append(0)
            else:  # stay in current state and no error
                received_bits.append(bit)

        return received_bits
