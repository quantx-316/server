class AlgoGenerator:
    """
    Creates fake algo information
    """

    def generate_algos(self, num_algos = 1):
        return [self.get_fake_algo() for _ in range(num_algos)]
    
    def get_fake_algo(self):
        return {
            "title": "test algo",
            "code": "def randCode(): pass"
        }
