import json

# first: model1 - llama2
#        model2 - vicuna
# second: model1 - vicuna
#         model2 - llama2

def process_json_objects(objs1, objs2):
    result = []

    vicuna_1 = 0
    vicuna_2 = 0

    for obj1 in objs1:
        for obj2 in objs2:
            if obj1['instruction'] == obj2['instruction']:
                if obj1['preference'] == obj2['preference']:
                    if int(obj1['preference']) == 2:
                        vicuna_1 += 1
                    
                    if int(obj2['preference']) == 1:
                        vicuna_2 += 1

                    result.append([
                        obj1['instruction'],
                        obj1['output_1'],
                        obj1['output_2'],
                        obj1['preference'],
                        obj2['preference']
                    ])
    print("vicuna_1", vicuna_1)
    print("vicuna_2", vicuna_2)
    return result

def main():
    with open(r'annotations1.json', 'r') as f1, open(r'annotations.json', 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    matching_objects = process_json_objects(data1, data2)

    for match in matching_objects:
        for i in range(len(match)):
            if isinstance(match[i], str):
                match[i] = match[i].replace('\n', '<br/>')

    print(len(matching_objects))
    # with open("vicuna-33b-v1.3_always_win_????.html", 'w') as f:
    with open("20230822-vicuna-33b-v1.3_vs_llama2-13b-chat.html", 'w') as f:
        f.write("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">
    </head>
    <body>
    <div class="container">
    <table class="table">
        <tr>
            <th>No.</th>
            <th>Instruction</th>
            <th>llama2 13b chat</th>
            <th>Vicuna 33b v1.3</th>
            <th>Invalid</th>
        </tr>
    """)
        for idx, result in enumerate(matching_objects):
            f.write(f"""
            <tr>
                <td>{idx+1}</td>
                <td>{result[0]}</td>
                <td>{result[1]}</td>
                <td>{result[2]}</td>
                <td>{result[3] == -1 or result[4] == -1}</td>
            </tr>
                    """)
        f.write("""
    </table>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-HwwvtgBNo3bZJJLYd8oVXjrBZt8cqVSpeBNS5n7C8IVInixGAoxmnlMuBnhbgrkm" crossorigin="anonymous"></script>
    </body>
    </html>
                """)

if __name__ == "__main__":
    main()
