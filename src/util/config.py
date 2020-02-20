import configparser

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.raw_data = self.config.get('FILES', 'raw_data')
        self.processed_data = self.config.get('FILES', 'processed_data')
        self.data_dir = self.config.get('FILES', 'data')
        self.intermediate_data = self.config.get('FILES', 'intermediate_data')
        self.external_data = self.config.get('FILES', 'external_files')

        self.comments_file = self.config.get('FILES', 'comments_file')
        self.videos_file = self.config.get('FILES', 'videos_file')

        self.user = self.config.get('DATABASE', 'username')
        self.password = self.config.get('DATABASE', 'password')
        self.host = self.config.get('DATABASE', 'host')

        self.report = self.config.get('REPORT', 'report')
        self.img_report = self.config.get('REPORT', 'img_report')

if __name__ == '__main__':
    c = Config()