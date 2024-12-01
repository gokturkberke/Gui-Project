from views.main_view import MainView
from viewmodels.main_viewmodel import MainViewModel
from models.database import setup_database

if __name__ == "__main__":
    setup_database()
    viewmodel = MainViewModel()
    app = MainView(viewmodel)
    app.mainloop()