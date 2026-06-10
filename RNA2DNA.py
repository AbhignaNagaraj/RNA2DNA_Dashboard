from biopandas.pdb import PandasPdb


def convert_rna_to_dna(file_input, output_file="DNA.pdb"):

    with open(file_input, "r") as fichier:
        atomes = fichier.readlines()

    output = []

    for atome in atomes:

        if (
            (atome[-1] == 'H' or atome[-4] == 'H')
            and ("U" in atome)
            and ("H5 " in atome)
        ):

            line = atome.split('   ')

            line[1] = line[1][:-2] + 'C7'

            line[-1] = '  C \n'

            atome = '   '.join(line)

        if "U" in atome:

            atome = atome[:19] + 'T' + atome[20:]

        output.append(atome)

    with open("pre-DNA1.pdb", "w") as fichier:

        fichier.writelines(output)

    atom_to_remove = ["O2'"]

    with open(
        'pre-DNA1.pdb', 'r'
    ) as oldfile, open(
        'pre-DNA2.pdb', 'w'
    ) as newfile:

        for line in oldfile:

            if not any(
                atom in line
                for atom in atom_to_remove
            ):

                newfile.write(line)

    ppdb = PandasPdb()

    ppdb.read_pdb('pre-DNA2.pdb')

    data = ppdb.df['ATOM']

    data["residue_name"] = data[
        "residue_name"
    ].replace(
        ['A'], 'DA'
    )

    data["residue_name"] = data[
        "residue_name"
    ].replace(
        ['T'], 'DT'
    )

    data["residue_name"] = data[
        "residue_name"
    ].replace(
        ['G'], 'DG'
    )

    data["residue_name"] = data[
        "residue_name"
    ].replace(
        ['C'], 'DC'
    )

    ppdb.to_pdb(
        path=output_file
    )

    return output_file


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "file_input",
        help="Input RNA PDB"
    )

    args = parser.parse_args()

    convert_rna_to_dna(
        args.file_input
    )