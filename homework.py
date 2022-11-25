class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self: object,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed:float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    
    def get_message(self: object) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {round(self.duration, 3)} ч.; '
                f'Дистанция: {round(self.distance, 3)} км; '
                f'Ср. скорость: {round(self.speed, 3)} км/ч; '
                f'Потрачено ккал: {round(self.calories, 3)}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    

    def __init__(self: object,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self: object) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self: object) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self: object) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self: object) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    HOURS_IN_MIN: int = 60
    def __init__(self: object,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self: object) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() +
                 self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM *
                (self.duration * self.HOURS_IN_MIN))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    KM_HOURS_IN_M_SECONDS: float = 3.6
    HOURS_IN_MIN: int = 60
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_WEIGHT_MEAN_SPEED_HEIGHT_MULTIPLIER: float = 0.029 

    def __init__(self: object,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self: object) -> float:
        return (((self.CALORIES_WEIGHT_MULTIPLIER * self.weight +
                 (self.get_mean_speed()**2 / self.height) *
                  self.CALORIES_WEIGHT_MEAN_SPEED_HEIGHT_MULTIPLIER
                  * self.weight) * (self.duration * self.HOURS_IN_MIN)))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_COEFFICENT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2
    
    def __init__(self: object,
                 action: int,
                 duration: float,
                 weight: float,
                 lenght_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool
    
    def get_mean_speed(self: object) -> float:
        return (self.lenght_pool * self.count_pool / self.M_IN_KM / self.duration)
    
    def get_spent_calories(self: object) -> float:
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_COEFFICENT) * self.CALORIES_WEIGHT_MULTIPLIER * self.weight * self.duration)



def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types = {
        'SWM':Swimming,
        'RUN':Running,
        'WLK':SportsWalking
    }
    return workout_types[workout_type](*data) 


def main(training: Training) -> None:
    """Главная функция."""
    info: object = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: dict = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: object = read_package(workout_type, data)
        main(training)

