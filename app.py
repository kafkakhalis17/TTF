from flask import Flask, render_template,request, send_from_directory, url_for
import time
import nltk 

# import from Class
from Search import Search
app = Flask(__name__)




# Run the page 
@app.route("/", methods=['GET', 'POST'])
def page():
   image_url = url_for('static', filename='assets/background-potrait.jpg')
   d_search = None
   flag_dataset, flag_twitter = None, None
   waktu = None
   data_traffic = None
   list_flag = None
   process_search = None
   if request.method == 'POST':
      d_search = request.form['search']
      waktu =  time.strftime('%H:%M:%S')

      process_search = Search(d_search, waktu)
      data_traffic, flag_dataset, flag_twitter  = process_search.search_word()
      if len(data_traffic) == 0:
         data_traffic = "Pada saat ini tidak ada data yang cocok dan info traffic yang tidak ditemukan, coba cari di lain waktu"
         list_flag = False
         
      # Proses data search
      # search = search_processing(d_search)
   return render_template("index.html", search=d_search, waktu=waktu, data_traffic = data_traffic, image_url=image_url, list_flag = list_flag, flag_dataset= flag_dataset, flag_twitter= flag_twitter)

if __name__ == "__main__":
   app.run(debug=True)