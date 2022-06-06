"""
Generates a name text file for a gff file
"""
import argparse


def parse_gff(fn):
    """
    parses a well formatted gff3 file, skips comment lines and ignores
    fasta lines. manifests attributes list as a dictionary for easier
    access of record attributes. individual representation records are in form

    [seq_id, source, type, start, end, score, strand, phase, {attribute_name: value, attribute_name2: value2}]
    """
    gff_representation = []
    with open(fn, "r") as gff:
        for line in gff:
            line = list(filter(None, line.split("\t")))
            if line[0] == "##FASTA\n":
                break
            if line[0][0:2] == "##":
                continue
            if line[2] not in ["CDS"]:
                continue

            details = line[8].split(";")
            attributes = {}
            for record in details:
                record = record.split("=")
                attributes[record[0]] = record[1].strip("\n")

            line[8] = attributes
            gff_representation.append(line)

    return gff_representation


def build_names(gff, strain):
    """
    Builds name record in the form below and returns a list of all such records
    in the gff representation list passed in

    [[searchable, attributes, here], strain, id/name, seq_id, start, end]
    """
    names = []

    for record in gff:
        temp = []
        temp.append(get_desired_attributes(record[8]))
        temp.append(strain)
        temp.append(record[8]["Name"]) if "Name" in record[8] else temp.append(
            record[8]["ID"]+"_gene")
        temp.append(record[0])
        temp.append(record[3])
        temp.append(record[4])
        names.append(temp)

    return names


def get_desired_attributes(attributes):
    attrs = []

    # ADD ANY OTHER DESIRED SEARCHABLE ATTRIBUTES HERE
    if "Name" in attributes:
        attrs.append(attributes["Name"])
    attrs.append(attributes["ID"]+"_gene")
    attrs.append(attributes["ID"])
    if "product" in attributes:
        attrs.append(attributes["product"])

    return attrs


def partition_sequences(names):
    sequences = {}

    for record in names:
        if record[3] in sequences:
            sequences[record[3]].append(record)
        else:
            sequences[record[3]] = [record]

    return sequences


def write_names(fn, strain, names, label, method):

    names = partition_sequences(names)

    for seq_id in names:
        with open(f"data/tracks/{strain}/{label}/{seq_id}/{fn}", method) as f:
            for line in names[seq_id]:
                search = '","'.join(line[0])
                other = '","'.join(line[1:])
                out_string=f'[["{search}"],"{other}"]\n'
                f.write(out_string)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Build a names text file from a gff file.')
    parser.add_argument('--in', "-i", type=str, required=False, default="genes.gff",
                        help='the name of the GFF file to be processed (default: %(default)s)')
    parser.add_argument('--out', "-o", type=str, required=False, default="names.txt",
                        help='the name of the names file to write. NOTE: This should not be the full path and this program will prepend "data/tracks/strain/seq_id/" to the chosen name (default: %(default)s)')
    parser.add_argument('--strain', "-s", type=str, required=False, default="BBQS859",
                        help='the strain on which we are operating (default: %(default)s)')
    parser.add_argument('--label', '-l', type=str, required=False, default='Prokka',
                        help='the track label for the names being built. (default: %(default)s)')

    args = vars(parser.parse_args())
    gff = parse_gff(args["in"])
    names = build_names(gff, args["strain"])
    write_names(args["out"], args["strain"], names, args['label'], "w")
