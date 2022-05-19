def generate_numeric(numeric_cols, data, use=False):
    if use and len(numeric_cols) > 0:
        for fea1 in numeric_cols:
            data[str(fea1) + '_sqr'] = data[fea1]**2
            data[str(fea1) + '_sqrt'] = np.sqrt(np.abs(data[fea1]))
            for fea2 in numeric_cols:
                if fea1 != fea2:
                    data[str(fea1) + '_times_' + str(fea2)] = data[fea1] * data[fea2]
                    data[str(fea1) + '_div_' + str(fea2)] = data[fea1]
                    data[str(fea1) + '_div_' + str(fea2)][data[fea1] != 0] = data[fea1][data[fea2] != 0] / data[fea2][data[fea2] != 0]
    return data
