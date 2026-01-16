from .Model import LogImporter
from .Model import Math
from .View import PrimaryView

class Controller():

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.df_original = None
        self.df_sensores = None
        self.eixo_x = None
    
        self.config_offset = 0
        self.config_outlier_window = 0
        self.config_ma_window = 0
        self.config_calibration = None
        self.config_lowpass = None
        self.config_highpass = None
    
    def select_archive(self, sender, app_data):
        file_path = app_data['file_path_name']
        self.model.import_file(file_path)
        self.model.create_timestamp()
        self.eixo_x, self.df_sensores = self.model.join_files()

        if self.eixo_x is not None:
            self.df_original = self.df_sensores.copy()
            self.view.callback_checkbox(self.eixo_x, self.df_sensores)

            self._process_pipeline()
    
    def _process_pipeline(self):
        if self.df_original is None:
            return

        df_temp = self.df_original.copy()
        math_tool = Math(self.eixo_x, df_temp)

        if self.config_calibration:
            df_temp = math_tool.calibration(self.config_calibration)
            math_tool = Math(self.eixo_x, df_temp)
        
        if self.config_offset > 0:
            df_temp = math_tool.adjust_offset(self.config_offset)
        
        if self.config_outlier_window > 0:
            math_tool = Math(self.eixo_x, df_temp)
            df_temp = math_tool.remove_outliers(self.config_outlier_window, thresh=3, verbose=False)

        if self.config_ma_window > 0:
            math_tool = Math(self.eixo_x, df_temp)
            df_temp = math_tool.moving_average(self.config_ma_window)
        
        if self.config_lowpass:
            math_tool = Math(self.eixo_x, df_temp)
            df_temp = math_tool.lowpass_filter(cutoff_freq=self.config_lowpass, order=5)
        
        if self.config_highpass:
            math_tool = Math(self.eixo_x, df_temp)
            df_temp = math_tool.filter_high_pass(cutoff_freq=self.config_highpass, order=5)

        self.df_sensores = df_temp
        self.view.update_plot(self.eixo_x, self.df_sensores)

    def apply_offset(self, n_linhas):
        self.config_offset = int(n_linhas)
        self._process_pipeline()

    def apply_outliers(self, window, thresh=3, verbose=False):
        self.config_outlier_window = int(window)
        self._process_pipeline()

    def apply_move_average(self, sesh):
        self.config_ma_window = int(sesh)
        self._process_pipeline()
    
    def apply_calibration(self, factors):
        self.config_calibration = factors
        self._process_pipeline()
    
    def apply_lowpass(self, cutoff_freq, freq_rate=None, order=5):
        self.config_lowpass = cutoff_freq
        self._process_pipeline()
    
    def apply_highpass(self, cutoff_freq, freq_rate=None, order=5):
        self.config_highpass = cutoff_freq
        self._process_pipeline()

    def get_tendency_data(self):
        if self.df_sensores is None or self.eixo_x is None:
            return None

        math_tool = Math(self.eixo_x, self.df_sensores)
        
        return math_tool.get_tendency(window_size=None)