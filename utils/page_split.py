import pathlib
import json

def split_page(json_path: str, output_dir: str):
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    with open(json_path, "r") as file:
        input_data = file.read()

    # Returns a list
    output_list = json.loads(input_data)

    num_pages = output_list["billed_pages"]
    bbox_list = output_list["elements"]
    metadata_list = output_list["metadata"]["pages"]

    for page in range(1, num_pages + 1):
        new_output = copy.deepcopy(output_list)
        new_output["elements"] = []
        new_output["metadata"]["pages"] = []
        new_output["html"] = ""
        new_output["text"] = ""

        for bbox in bbox_list:
            if bbox["page"] == page:
                new_output["elements"].append(bbox)

        for metadata in metadata_list:
            if metadata["page"] == page:
                new_output["metadata"]["pages"].append(metadata)

        file_name = pathlib.Path(json_path).stem
        save_path = pathlib.Path(output_dir) / f"{file_name}/page_{page}.json"
        pathlib.Path(save_path).parent.mkdir(parents=True, exist_ok=True)  # json 저장 경로가 존재하지 않으면 생성
        with open(save_path, "w") as file:
            file.write(json.dumps(new_output, indent=4, ensure_ascii=False))