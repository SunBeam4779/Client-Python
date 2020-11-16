import pymysql

"""
simple script the insert data into the database
"""

path = "D:/python3/workspace/Client/Client/docs/202011061728.jpg"
ECG = "D:/My Documents/ECG Detector Project/data/ECG/Filtered/data332_Channel1_dec.txt"
# file = open(path, encoding='utf-8', errors='ignore')
# img = file.read()
# file.close()
connect = pymysql.connect(host='localhost', user='root', password='root', db='user')


def insert_img(path_):

    """
    insert the image into the database
    :param path_: the path of the image
    :return: none
    """

    cursor = connect.cursor()
    # cursor.execute("insert into img set imgs='%s'" % mysql.Binary(img))
    try:
        cursor.execute("Insert into profile(username, name, unique_id, profile_path) "
                       "values('%s', '%s', '%s', '%s')" % ('universal', 'yuhang', '4131130301', path_))
        connect.commit()
    except Exception as e:
        print("wrong!" + e.__str__())
    cursor.close()
    connect.close()


def insert_data():

    """
    Only for test. Insert the user's information into the database
    :return: none
    """

    cursor = connect.cursor()
    try:
        cursor.execute("Insert into userdata(username, name, unique_id, data_number, "
                       "data_type, value, checkable, synchronized) "
                       "values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %
                       ('universal', 'yuhang', '4131130301', '20201024141904',
                        'heart rate', '76', 'No', 'Yes'))
        connect.commit()
    except Exception as e:
        print("wrong!" + e.__str__())
    cursor.close()
    connect.close()


insert_data()
