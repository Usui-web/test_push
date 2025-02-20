import PySimpleGUI as sg
import numpy as np

def format_number():
    return  float("".join(var["front"]) + "." + "".join(var["back"])) if var["back"] else float("".join(var["front"]))

def update_display(display_value):
    try:
         window["_DISPLAY_"].update(value="{:,.4f}".format(display_value))
    except:
         window["_DISPLAY_"].update(value=display_value)

def number_click(event):
    global var
    if event in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        if var["decimal"]:
            var["front"].append(event)  # 整数部分に追加
        else:
            var["back"].append(event)   # 小数部分に追加
        update_display(format_number())

def decimal_click(event):
    global var
    if event == "." and var["decimal"]:  # 小数点ボタンが押されたとき
        var["decimal"] = False  # 小数点を入力後、小数部分に移行

def sankaku_click(event):
    global var
    if event == "np.sin(np.pi)":
        var["operator"] = "sin"
    elif event == "np.cos(np.pi)":
        var["operator"] = "cos"
    elif event == "np.tan(np.pi)":
        var["operator"] = "tan"
    
    # 現在の値を取得し、計算を行う
    if var["operator"] in ["sin", "cos", "tan"]:
        try:
            angle_in_degrees = format_number()
            angle_in_radians = np.radians(angle_in_degrees)  # 度をラジアンに変換
            if var["operator"] == "sin":
                result = np.sin(angle_in_radians)
            elif var["operator"] == "cos":
                result = np.cos(angle_in_radians)
            elif var["operator"] == "tan":
                result = np.tan(angle_in_radians)
            var["result"] = result
            update_display(result)
        except Exception as e:
            update_display("Error")

def operator_click(event):
    global var
    if event in ["+", "-", "*", "/", "%"]:
        var["operator"] = event
        var["x_val"] = format_number()
        clear_click()

def clear_click():
    global var
    var["front"].clear()
    var["back"].clear()
    var["decimal"] = True
    var["result"] = 0.0
    update_display(var["result"])

def calculate_click():
    global var
    var["y_val"] = format_number()
    try:
        var['result'] = eval(f"{var['x_val']} {var['operator']} {var['y_val']}")
        update_display(var['result'])
    except Exception as e:
        update_display("Error")

# Main function
if __name__ == "__main__":
    
    layout = [
        [sg.Text("0.0000", key="_DISPLAY_", size=(30, 1))],
        [sg.Button("7", key="7", size=(3, 1)), sg.Button("8", key="8", size=(3, 1)), sg.Button("9", key="9", size=(3, 1)), sg.Button("/", key="/", size=(3, 1))], 
        [sg.Button("4", key="4", size=(3, 1)), sg.Button("5", key="5", size=(3, 1)), sg.Button("6", key="6", size=(3, 1)), sg.Button("*", key="*", size=(3, 1))],
        [sg.Button("1", key="1", size=(3, 1)), sg.Button("2", key="2", size=(3, 1)), sg.Button("3", key="3", size=(3, 1)), sg.Button("+", key="+", size=(3, 1))],
        [sg.Button("0", key="0", size=(3, 1)), sg.Button(".", key=".", size=(3, 1)), sg.Button("-", key="-", size=(3, 1)), sg.Button("calc", key="calc", size=(3, 1))],
        [sg.Button("sin", key="np.sin(np.pi)", size=(3, 1)), sg.Button("cos", key="np.cos(np.pi)", size=(3, 1)), sg.Button("tan", key="np.tan(np.pi)", size=(3, 1))]
    ]

    window = sg.Window("簡単電卓", layout, size=(200, 200), background_color="#272533", return_keyboard_events=True)
    
    var = {"front": [], "back": [], "decimal": True, "x_val": 0.0, "y_val": 0.0, "result": 0.0, "operator": "+"}
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event in ['=', "calc"]:
            calculate_click()
        elif event in ["C", "CE"]:
            clear_click()
        elif event in ["np.sin(np.pi)", "np.cos(np.pi)", "np.tan(np.pi)"]:
            sankaku_click(event)
        
        number_click(event)
        decimal_click(event)
        operator_click(event)

    window.close()

