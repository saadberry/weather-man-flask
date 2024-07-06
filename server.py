import calendar
import os
import json

from flask import Flask, request, render_template

from main import GenerateReports, CalculateTemp

app = Flask(__name__)

class WeatherData:
    """
    Class responsible for handling weather data
    """
    def __init__(self) -> None:
        self.weather_data = {}
        self.process_data()

    def process_data(self):
        """
        Method that reads weather data
        from weather-files.txt, and stores
        them in self.weather_data
        """
        current_directory = os.getcwd()
        file_path = f"{current_directory}/weather-data.txt"
        # if self.weather_data:
        #     return
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data_str = file.read()
                self.weather_data = json.loads(data_str)
        else:
            raise Exception(f"File '{file_path}' does not exist.")

class MyRoutes:
    """
    Class containing our routes
    """
    def __init__(self, app):
        self.app = app
        self.setup_routes()



    def setup_routes(self):
        """
        Method that sets up routes
        """
        self.app.add_url_rule('/', 'hello_world', self.hello_world)
        self.app.add_url_rule('/task1', 'task_one', self.task_one)
        self.app.add_url_rule('/task2', 'task_two', self.task_two)
        self.app.add_url_rule('/task3', 'task_three', self.task_three)
        self.app.add_url_rule('/multiple_reports', 'multiple_reports', self.multiple_reports)
        self.app.add_url_rule('/api/query', 'query db', self.query_db, methods=['POST'])


    def hello_world(self):
        # return render_template('index.html')

    def query_db(self):
        """
        Endpoint that accepts a query from the UI
        """
        data = request.get_json()
        options = data.get('options', [])
        print(f'options: {options}')
        if len(options) == 1:
            for option in options:
                if option == 'one':
                   return self.task_one(default=True)
                # elif option == 'two':

                # elif option == 'three':
        return {"status": 200}
        
    def task_one(self, default=False):
        """
        Method that queries for task one
        Parameters:
            - y (number) : year
        """
        weather_data = WeatherData()
        report = GenerateReports()
        calc_temp = CalculateTemp(weather_data, report)
        if default:
            year = str(2010)
        else:
            year = request.args.get('y')
        print(f'year: {year}, type: {type(year)}')
        report.generate_report(1, calc_temp.task_one(year))
        result = report.display_report(cli=False)
        months = list(calendar.month_name)
        
        print(f'result: {result}')
        # self.weather_data
        # return f'<h1> Result: </h1> <h2>{result}</h2>'
        return render_template('report.html', result=result, months=months, show_task_one=True, show_task_two=False)

    def task_two(self):
        """
        Method that queries for task two
        Parameters:
            - y (number) : year
            - m (number) : month
        """
        weather_data = WeatherData()
        report = GenerateReports()
        calc_temp = CalculateTemp(weather_data, report)

        year = request.args.get('y')
        month = request.args.get('m')

        date_to_be_queried = f'{year}/{month}'
        report.generate_report(2, calc_temp.task_two(date_to_be_queried))
        result = report.display_report(cli=False)

        return render_template('report.html', result=result, show_task_one=False, show_task_two=True)

    def task_three(self):
        """
        Method that queries for task two
        Parameters:
            - y (number) : year
            - m (number) : month        
        """
        weather_data = WeatherData()
        report = GenerateReports()
        calc_temp = CalculateTemp(weather_data, report)

        year = request.args.get('y')
        month = request.args.get('m')
        date_to_be_queried = f'{year}/{month}'
        report.generate_report(3, calc_temp.task_three(date_to_be_queried))
        result = report.display_report(cli=False)

        return render_template('report.html', result=result, show_task_one=False, show_task_two=False, show_task_three=True, len=len)

    def multiple_reports(self):
        """
        Method that handles multiple queries
        Example: 
            -multiple_reports?task1=true&y1=2008&task2=true&y2=2008&m2=10&task3=true&y3=2008&m3=10
        """
        print(f'in method')

        weather_data = WeatherData()
        report = GenerateReports()
        calc_temp = CalculateTemp(weather_data, report)

        # Parsing request
        task_one = request.args.get('task1')
        if task_one:
            year_one = request.args.get('y1')
            print(f'YAER: {year_one}')
            report.generate_report(1, calc_temp.task_one(year_one))

        task_two = request.args.get('task2')
        if task_two:
            year_two = request.args.get('y2')
            month_two = request.args.get('m2')
            date_to_be_queried = f'{year_two}/{month_two}'
            report.generate_report(2, calc_temp.task_two(date_to_be_queried))

        task_three = request.args.get('task3')
        if task_three:
            year_three = request.args.get('y3')
            month_three = request.args.get('m3')
            date_to_be_queried = f'{year_three}/{month_three}'
            report.generate_report(3, calc_temp.task_three(date_to_be_queried))

        result = report.display_report(cli=False)
        print(f'result: {result}')
        months = list(calendar.month_name)

        return render_template('report.html', result=result, show_task_one=task_one, show_task_two=task_two, show_task_three=task_three, len=len, months=months)







# Initialize the routes
routes = MyRoutes(app)

# if __name__ == '__main__':
#     app.run(debug=True)
