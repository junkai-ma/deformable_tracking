import numpy


def Distance_Transform_L1(sample_function):
    distance = sample_function
    (height, width) = sample_function.shape
    location_row = numpy.zeros(sample_function.shape, dtype='int')
    location_column = numpy.zeros(sample_function.shape, dtype='int')
    # calculate the distance in each row
    for row_num in range(height):
        for column_num in range(1, width):
            # forward
            if distance[row_num, column_num] >= distance[row_num, column_num-1]-1:
                location_column[row_num, column_num] = column_num
                location_row[row_num, column_num] = row_num
            else:
                distance[row_num, column_num] = distance[row_num, column_num-1]-1
                location_column[row_num, column_num] = location_column[row_num, column_num-1]
                location_row[row_num, column_num] = row_num

        for column_num in range(width-2, -1, -1):
            # backward
            if distance[row_num, column_num] <= distance[row_num, column_num+1]-1:
                distance[row_num, column_num] = distance[row_num, column_num+1]-1
                location_column[row_num, column_num] = location_column[row_num, column_num+1]
                location_row[row_num, column_num] = row_num

    for column_num in range(width):
        for row_num in range(1, height):
            # forward
            if distance[row_num, column_num] >= distance[row_num-1, column_num]-1:
                location_row[row_num, column_num] = row_num
            else:
                distance[row_num, column_num] = distance[row_num-1, column_num]-1
                location_row[row_num, column_num] = location_row[row_num-1, column_num]
                location_column[row_num, column_num] = location_column[row_num-1, column_num]

        for row_num in range(height-2, -1, -1):
            # backward
            if distance[row_num, column_num] <= distance[row_num+1, column_num]-1:
                distance[row_num, column_num] = distance[row_num+1, column_num]-1
                location_row[row_num, column_num] = location_row[row_num+1, column_num]
                location_column[row_num, column_num] = location_column[row_num+1, column_num]

    return distance, location_row, location_column

if __name__ == '__main__':
    import numpy as np
    sample = np.array([[5, 9, 13, 15],
                       [7, 18, 33, 17],
                       [9, 35, 34, 8],
                       [20, 18, 16, 5]])

    d, r, c = Distance_Transform_L1(sample)
    print d
    print r
    print c
