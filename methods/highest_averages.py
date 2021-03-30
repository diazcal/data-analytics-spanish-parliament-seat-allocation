class METHODS:
    DHONDT = "dhondt"
    SAINTELAGUE = "slague"

class HighestAverage:
    def __init__(self):
        self._ready_for_calc = False
        self._seat_allocation = None

    def get_seat_distribution(self, method=None):
        """
        dictionary in the same order it was given.
        :return: dictionary with seat allocation.
        """
        if method:
            if self._ready_for_calc:
                self._calculate(method, self.threshold)
        return self._seat_allocation

    def set_distribution_parameters(self, valid_votes, seats, party_and_votes_dict, threshold=None):
        """
        :param valid_votes: (int) total number of valid votes.
        :param seats: (int) total number of seats to allocate.
        :param party_and_votes_dict: (dict) dictionary with the parties and its votes
        with the format {"party_name": votes} E.g. {"CoolParty": 876, "AwesomeParty": 1098}
        :param threshold: (float) unitary limit to discard a party from being counted. E.g threshold=0.03 would mean
        that a party needs to have more than 3% of the total of valid votes to be taken into account for the seat
        allocation.
        """
        self._seat_allocation = None
        self.valid_votes = valid_votes
        self.seats = seats
        self.party_and_votes_dict = party_and_votes_dict
        self.threshold = threshold
        self._ready_for_calc = True

    def _calculate(self, method, threshold):
        """
        Seat calculation.
        """
        next_seat_quotients = self._seat_quotients(threshold)
        self._seat_allocation = {party: 0 for party in self.party_and_votes_dict.keys()}

        for seat in range(1, self.seats+1):
            next_seat_quotients.sort(key=lambda val: val[1], reverse=True)
            seat_winner = next_seat_quotients[0][0]
            self._seat_allocation[seat_winner] = self._seat_allocation[seat_winner] + 1
            party_votes = self.party_and_votes_dict[seat_winner]
            current_seat = self._seat_allocation[seat_winner]
            updated_seat_winner_quotient = self._algorithm(party_votes, current_seat, method)
            next_seat_quotients[0][1] = updated_seat_winner_quotient

        self._calc_ready = True

    def _seat_quotients(self, threshold):
        seat_quotients = [[party, quotient] for party, quotient in self.party_and_votes_dict.items()]
        if threshold:
            vote_limit = self.valid_votes * threshold
            for index, v in enumerate(seat_quotients):
                if v[1] < vote_limit:
                    break
            del seat_quotients[index:]
        return seat_quotients

    def _algorithm(self, party_votes, current_seat_allocation, method):
        if method == METHODS.DHONDT:
            quotient = self._dhondt(party_votes, current_seat_allocation)
        elif method == METHODS.SAINTELAGUE:
            quotient = self._saintelague(party_votes, current_seat_allocation)
        return quotient

    def _dhondt(self, party_votes, current_seat_allocation):
        """
        D'Hondt quotient assignment algorithm.

        :param party_votes: Total votes of a given party.
        :param current_seat_allocation: Number of current seats.
        :return: New quotient for the next seat allocation round.
        """
        quotient = party_votes / (current_seat_allocation + 1)
        return quotient

    def _saintelague(self, party_votes, current_seat_allocation):
        """
        Sainte-Laguë quotient assignment algorithm.

        :param party_votes: Total votes of a given party.
        :param current_seat_allocation: Number of current seats.
        :return: New quotient for the next seat allocation round.
        """
        quotient = party_votes / (2*current_seat_allocation + 1)
        return quotient
