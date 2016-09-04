import re


class WLS(object):

    def __init__(self):
        self.word_pos = {}
        self.level_stat = {}

    def get_word_positions(self, corpus):
        tokens = re.findall('\w+', corpus)
        for i,tok in enumerate(tokens):
            self.word_pos.setdefault(tok, []).append(i)

    def compute_spectra(self):

        if not self.word_pos:
            return None

        # Total number of words.
        self._N = sum([len(self.word_pos[w]) for w in self.word_pos])

        # Compute level statistics
        for k in self.word_pos:
            self.level_stat[k] = self._word_spectrum(k)

    def _word_spectrum(self, word):
        pos = self.word_pos[word]
        n = len(pos)
        wls = { 'count': n, 'C': 0, 'sigma_nor': 0 }
        if n > 2:
            d = [(pos[i+1] - pos[i]) for i in xrange(n-1)]  # distance distribution
            avg = sum(d) / float(n - 1)  # len(d) = n-1 (start calculation from second word)
            s = sum([(k - avg)**2 for k in d])/float(n-2)  # non-biased variance estimator
            sigma = (s**.5) / avg
            p = float(n) / self._N
            wls['sigma_nor'] = sigma/((1 - p)**.5)  # formula (2)
            wls['C'] = (wls['sigma_nor'] - (2*n - 1.)/(2*n + 2.))\
                        * (n**.5 * (1 + 2.8 * n**-0.865))  # formula (4)
        return wls

    def extract(self, corpus):
        self.get_word_positions(corpus)
        self.compute_spectra()
        return sorted(self.level_stat.items(), key=lambda x: x[1]['C'], reverse=True)


if __name__ == "__main__":

    with open('Relativity.test', 'rb') as f:
        corpus = f.read().lower()

    wls = WLS().extract(corpus)

    out_file = 'Relativity.out'
    print "Writing output to {}".format(out_file)
    with open(out_file, 'wb') as f:
        f.write("word\tC\tcount\tsigma_nor\n")
        for k, v in wls:
            line = "{}\t{}\t{}\t{}\n".format(k, v['C'], v['count'], v['sigma_nor'])
            f.write(line)
