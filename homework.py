from dataclasses import dataclass
from typing_extensions import Final, ClassVar
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TRAINING_TYPE: Final[str] = "Тип тренировки"
    DURATION: Final[str] = "Длительность"
    DISTANCE: Final[str] = "Дистанция"
    SPEED: Final[str] = "Ср. скорость"
    CALORIES: Final[str] = "Потрачено ккал"

    def get_message(self: object) -> str:
        """Возвращает сообщениие об итогах тренировки."""
        return (
            f"{self.TRAINING_TYPE}: {self.training_type}; "
            f"{self.DURATION}: {self.duration:.3f} ч.; "
            f"{self.DISTANCE}: {self.distance:.3f} км; "
            f"{self.SPEED}: {self.speed:.3f} км/ч; "
            f"{self.CALORIES}: {self.calories:.3f}."
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: Final[int] = 1000
    MIN_IN_H: Final[int] = 60

    def __init__(
        self: object,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        """Инициализация необходимых данных.

        Инициализирует кол-во действий, длительности и веса.
        """
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self: object) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self: object) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self: object) -> float:
        """Получить количество затраченных калорий."""
        raise ValueError(
            "Вызов метода родительского класса запрещён. "
            "Необходимо переопределить метод в дочернем классе."
        )

    def show_training_info(self: object) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: Final[int] = 18
    CALORIES_MEAN_SPEED_SHIFT: Final[float] = 1.79

    def get_spent_calories(self: object) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * (self.duration * self.MIN_IN_H)
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    KMH_IN_MSEC: Final[float] = 0.278
    CM_IN_M: Final[int] = 100
    CALORIES_WEIGHT_MULTIPLIER: Final[float] = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: Final[float] = 0.029

    def __init__(
        self: object,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:
        """Инициализация необходимых данных.

        Инициализирует кол-во действий,
        длительность, вес и рост пользователя.
        """
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self: object) -> float:
        """Получить количество затраченных калорий."""
        return (
            self.CALORIES_WEIGHT_MULTIPLIER * self.weight
            + (
                (self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                / (self.height / self.CM_IN_M)
            )
            * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
            * self.weight
        ) * (self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT: Final[float] = 1.1
    CALORIES_WEIGHT_MULTIPLIER: Final[int] = 2

    def __init__(
        self: object,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ) -> None:
        """Инициализация необходимых данных.

        Инициализирует кол-во действий, длительность,
        вес, длину бассейна и кол-во его проплытий.
        """
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self: object) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self: object) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
            * self.duration
        )


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_training_cls_map = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }
    try:
        return workout_type_training_cls_map[workout_type](*data)
    except KeyError:
        raise ValueError("Неверно передан код тренировки.")


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLKs", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: object = read_package(workout_type, data)
        main(training)
