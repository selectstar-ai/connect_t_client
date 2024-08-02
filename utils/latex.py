
from pathlib import Path 
import matplotlib.pyplot as plt

def visualize_latex(latex_equation: str,
                    file_path: str,
                    cache_dir: str,
                    ): 
    """
    Latex 수식을 png 파일 형태로 시각화합니다. 
    """
    try:
        with open("assets/latex_string.txt", "r") as f: 
            target_list = f.read().split("\n")
        
        for target in target_list:
            latex_equation = latex_equation.replace(target, f"{target} ")

        latex_equation = fr"${latex_equation}$"
        fig, ax = plt.subplots()

        ax.text(0.5, 0.5, 
                latex_equation, 
                fontsize=20, 
                ha='center', 
                va='center'
                )

        # hide axis 
        ax.axis('off')

        # download the image 
        # plt.rc("text", usetex=True)
        plt.show()
        save_path = str(Path(cache_dir) / (Path(file_path).stem + "_latex" + Path(file_path).suffix))
        ax.figure.savefig(save_path,
                        bbox_inches='tight')
        plt.close()
    
        return save_path
    except Exception as e:
        print(f"Failed to visualize latex equation: {e}")
        plt.close()
        return None