"""
appends to a name text file with searchable names for bed generated tracks
"""
import argparse
import build_gff_names as gff
import bed_to_json as bed


def build_names(bed_data, strain):
    """
    Builds name record in the form below and returns a list of all such records
    in the bed data representation list passed in

    [[searchable, attributes, here], strain, id/name, seq_id, start, end]
    """
    names = []

    for seq_id in bed_data:
        for record in bed_data[seq_id]:
            temp = []
            temp.append([record[4],record[5],record[11].strip("\n")])
            temp.append(strain)
            temp.append(record[4])
            temp.append(record[8])
            temp.append(str(record[1]))
            temp.append(str(record[2]))
            names.append(temp)

    return names


def write_names(fn, strain, names, label, method):

    names = gff.partition_sequences(names)

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
    parser.add_argument('--in', "-i", type=str, required=False, default="features.bed",
                        help='the name of the BED file to be processed (default: %(default)s)')
    parser.add_argument('--out', "-o", type=str, required=False, default="names.txt",
                        help='the name of the names file to write. NOTE: This should not be the full path and this program will prepend "data/tracks/strain/seq_id/" to the chosen name (default: %(default)s)')
    parser.add_argument('--strain', "-s", type=str, required=False, default="BBQS859",
                        help='the strain on which we are operating (default: %(default)s)')
    parser.add_argument('--label', '-l', type=str, required=True,
                        help='the track label for the names being built. Required.')

    args = vars(parser.parse_args())
    bed_data = bed.read_bed(args["in"])
    names = build_names(bed_data, args["strain"])
    write_names(args["out"], args["strain"], names, args['label'], "w")
