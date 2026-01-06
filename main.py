from tests import Teste_view, Teste_controller, Teste_Model

view = Teste_view.PrimaryView()
controller = Teste_controller.Controller()

if __name__ == "__main__":
   
    view.set_callback(controller.select_archive)
    view.build_window()
    view.run()
