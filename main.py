import sys
import os

sys.path.append(os.getcwd())


from dashboard_instrumentacao.Model import LogImporter
from dashboard_instrumentacao.View import PrimaryView
from dashboard_instrumentacao.Controller import Controller

def main():
    model = LogImporter()
    view = PrimaryView()
    controller = Controller(model, view)

    view.set_callback(controller.select_archive, controller.apply_offset, controller.apply_outliers, controller.apply_move_average)

    view.build_window()
    view.run()

if __name__ == "__main__":
    main()