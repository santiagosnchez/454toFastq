
import sys
import gzip
from itertools import izip

def delspace(x):
    if ' ' in x:
        x.remove(' ')
        return delspace(x)
    elif '' in x:
        x.remove('')
        return delspace(x)
    else:
        return x

basefile = sys.argv[1]
c = 0
h = ''
seqc = {}
quac = {}
with gzip.open(basefile+".fastq.gz","w") as fqgz:
    with open(basefile+".fna","r") as fasta, open(basefile+".qual","r") as qual:
        for f,q in izip(fasta,qual):
            if ">" in f and ">" in q:
                if seqc.get(h) and quac.get(h):
                    fqgz.write(seqc[h] + "\n+\n" + quac[h] + "\n")
                    del seqc[h]
                    del quac[h]
                    c += 1
                    sys.stdout.write(" {:<17s}done for {} reads\r".format("[454toFastq.py]",c)),
                    sys.stdout.flush()
                    h = f.rstrip()
                    seqc[h] = ''
                    quac[h] = ''
                    fqgz.write("@"+f[1:])
                else:
                    h = f.rstrip()
                    seqc[h] = ''
                    quac[h] = ''
                    fqgz.write("@"+f[1:])
            else:
                seqc[h] += f.rstrip()
                q = delspace(q.rstrip().split(" "))
                quac[h] += ''.join(map(lambda i: chr(int(i)+33), q))
print ''
