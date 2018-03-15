
import sys
import gzip

def keyisfound(x, key):
    try:
        x[key]
        return True
    except KeyError:
        return False

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
seqc = {}
quac = {}
h = ''
with gzip.open(basefile+".fastq.gz","w") as fqgz:
    with open(basefile+".fna") as fasta, open(basefile+".qual") as qual:
        for f,q in zip(fasta,qual):
            if ">" in f and ">" in q:
                if keyisfound(seqc, h) and keyisfound(quac, h):
                    fqgz.write(seqc[h] + "\n+\n" + quac[h] + "\n")
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
