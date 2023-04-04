from io import BytesIO
import matplotlib.pyplot as plt
import base64
import pandas as pd
import urllib
import urllib.error
import urllib.request

import folium

# Google API Modules
#from pygeocoder import Geocoder
import googlemaps

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

###----------------------
#
#    get_GPS()
#        create new DataFrame with columns = ["id", "lat", "lon"]
#            lat : latitude
#            lon : longitude
#
###----------------------
def get_GPS(arr, df):

    #arr = "75015"
    print(f"arr={arr}")
    sr0 = df['id']
    sr1 = df['address_zipcode']
    sr2 = df['lat_lon']

    #print(f"type(sr1)={type(sr1)}")
    df_GPS = sr0.to_frame()
    df_GPS = pd.concat([df_GPS, sr1], axis=1)
    df_GPS = pd.concat([df_GPS, sr2], axis=1)
    df_GPS = pd.concat([df_GPS, df_GPS["lat_lon"].str.split(",", expand=True)], axis=1)
    df_GPS.drop(columns='lat_lon', inplace=True)
    df_GPS = df_GPS.rename(columns={0:'lat', 1:"lon"})
    #df_GPS = pd.concat([df_GPS, sr2], axis=1)

    print(f"df_GPS.dtypes=\n{df_GPS.dtypes}")
    #print(df_GPS)

    #list_GPS = visualize_locations(id, df_GPS)
    list_GPS = visualize_locations(arr, df_GPS)

    return

def get_GPS_bk(id, df):


    #print(f"df.dtypes={df.dtypes}")
    sr1 = df['id']
    sr2 = df['lat_lon']

    #print(f"type(sr1)={type(sr1)}")
    df_GPS = sr1.to_frame()
    df_GPS = pd.concat([df_GPS, sr2], axis=1)
    df_GPS = pd.concat([df_GPS, df_GPS["lat_lon"].str.split(",", expand=True)], axis=1)
    df_GPS.drop(columns='lat_lon', inplace=True)
    df_GPS = df_GPS.rename(columns={0:'lat', 1:"lon"})
    #df_GPS = pd.concat([df_GPS, sr2], axis=1)

    #print(f"df_GPS.dtypes={df_GPS.dtypes}")
    #print(df_GPS)

    list_GPS = visualize_locations(id, df_GPS)

    return



def visualize_locations(arr, df_GPS,  zoom=13):

    #print(f"+++++++++++++++GPS=\n{df_GPS}")
    df_GPS = df_GPS[df_GPS['address_zipcode']==arr]
    print(f"df_GPS=\n{df_GPS}")

    #list_GPS = df_GPS.iloc[0].to_list()
    #lat = list_GPS[1]
    #lon = list_GPS[2]

    #print("#--------------------------#")
    #print(f"lat={lat}  lon={lon}")
    #print("#--------------------------#")


    # 図の大きさを指定する。
    f = folium.Figure(width=1000, height=500)

    # 初期表示の中心の座標を指定して地図を作成する。
    #center_lat=34.686567
    #center_lon=135.52000
    center_lat=48.855351
    center_lon=2.345894
    m = folium.Map([center_lat,center_lon], zoom_start=zoom).add_to(f)

    print(f"df_GPS.shape[0]={df_GPS.shape[0]}")
    for i in range(df_GPS.shape[0]):
        lat = df_GPS.iloc[i, 2]
        lon = df_GPS.iloc[i, 3]
        folium.Marker(location=[lat,lon]).add_to(m)

    #print(f"++++++++++++ m={m}")
    path_map = '/Users/katsuji/Django/Greta78/GretaProj7/MyProj/main/templates/main/'
    m.save(path_map + "/map1.html")

    return m

def visualize_locations_bk(id, df_GPS,  zoom=12):

    #print(f"+++++++++++++++GPS=\n{df_GPS}")
    GPS = df_GPS[df_GPS['id']==id]
    print(f"\nGPS=\n{GPS}")

    list_GPS = GPS.iloc[0].to_list()
    lat = list_GPS[1]
    lon = list_GPS[2]

    print("#--------------------------#")
    print(f"lat={lat}  lon={lon}")
    print("#--------------------------#")


    # 図の大きさを指定する。
    f = folium.Figure(width=1000, height=500)

    # 初期表示の中心の座標を指定して地図を作成する。
    #center_lat=34.686567
    #center_lon=135.52000
    center_lat=48.855351
    center_lon=2.345894
    m = folium.Map([center_lat,center_lon], zoom_start=zoom).add_to(f)

    folium.Marker(location=[lat,lon]).add_to(m)

    print(f"++++++++++++ m={m}")
    path_map = '/Users/katsuji/Django/Greta78/GretaProj7/MyProj/main/templates/main/'
    m.save(path_map + "/map1.html")

    return m

def download_image(id, df_GPS):

    #print(f"+++++++++++++++GPS=\n{df_GPS}")
    GPS = df_GPS[df_GPS['id']==id]
    print(f"\nGPS=\n{GPS}")

    list_GPS = GPS.iloc[0].to_list()
    lat = list_GPS[1]
    lon = list_GPS[2]

    print("#--------------------------#")
    print(f"lat={lat}  lon={lon}")
    print("#--------------------------#")

    # htmlの設定
    html1 = 'https://maps.googleapis.com/maps/api/staticmap?center='

    # maptypeで取得する地図の種類を設定
    html2 = '&maptype=hybrid'

    # sizeでピクセル数を設定
    html3 = '&size='

    # sensorはGPSの情報を使用する場合にtrueとするので今回はfalseで設定
    html4 = '&sensor=false'

    # zoomで地図の縮尺を設定
    html5 = '&zoom='

    # マーカーの位置の設定（マーカーを表示させてくなければ無でも大丈夫）
    html6 = '&markers='

    # key="googleから取得したキーコード"となるように設定
    html7 = '&key='

    # 緯度経度の情報をセット
    axis = str(lat) + "," + str(lon)

    # url
    url = html1 + axis + html2 + html3 + pixel + html4 + html5 + scale + html6 + axis + html7 + googleapikey

    loc = "XXX"
    # pngファイルのパスを作成
    dst_path = output_path + '\\' + str(loc) + ".png"

    # 画像を取得しローカルに書き込み
    
    
    try:
        data = urllib.request.urlopen(url).read()
        with open(dst_path, mode="wb") as f:
            f.write(data)

    except urllib.error.URLError as e:
        print(e)
    

    return list_GPS  