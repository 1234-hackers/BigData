def generate_data(col):
    
    def get_cusor(col):
        csr_found = col.find().limit(20)
        return csr_found

    def get_time():
        now = datetime.now()
        fmt = now.strftime("%d/%m/%Y%H:%M:%S")
        return (now)

    def try_connection():
        if client:
            return "connected"
        else:
            return "error"
    def write_json(csr_found):
        cond = try_connection()
        if cond == "conected":
            new = list(csr_found)
            json_data = dumps(new, indent = 2)
            de_time = get_time()
            de_time = str(de_time)
            de_time = de_time.replace("-" , "")
            de_time = de_time.replace(":" , "")
            de_time = de_time.replace("." , "")
            with open('jsonData/'+ de_time +'.json', 'w') as file:
                file.write(json_data)
                file.close()
            write_json()
            return st.success("New Data Collected. Upload Latest File For Analysis")

        if cond == "error":
                return st.error("Could Not Connect To Database")

    def update_now():
        st.balloons()
        st.progress(99)        
        the_data = get_cusor(col)
        return write_json(the_data)