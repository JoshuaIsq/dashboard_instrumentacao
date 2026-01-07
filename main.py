# Arquivo: main.py
import sys
import os



def main():
    model = Model.LogImporter()
    view = View.PrimaryView()
    controller = Controller.Controller(model, view)
   
    # 3. Conectar o callback (Injeção de dependência)
    view.set_callback(controller.select_archive)
    view.build_window()
    view.run()

if __name__ == "__main__":
    main()