-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Мар 05 2026 г., 13:19
-- Версия сервера: 8.0.30
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `sport_rental`
--

-- --------------------------------------------------------

--
-- Структура таблицы `customers`
--

CREATE TABLE `customers` (
  `customer_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `customers`
--

INSERT INTO `customers` (`customer_id`, `user_id`, `phone`, `email`) VALUES
(1, 2, '+7(999)444-55-66', 'anna@mail.ru'),
(2, 3, '+7(999)555-66-77', 'petr@mail.ru'),
(3, 1, '+7(999)888-99-00', 'ivan@mail.ru');

-- --------------------------------------------------------

--
-- Структура таблицы `employees`
--

CREATE TABLE `employees` (
  `employee_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `position` varchar(100) DEFAULT NULL,
  `hire_date` date DEFAULT NULL,
  `point_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `employees`
--

INSERT INTO `employees` (`employee_id`, `user_id`, `position`, `hire_date`, `point_id`) VALUES
(1, 1, 'Старший сотрудник', '2023-01-15', 1),
(2, 3, 'Администратор', '2022-11-01', 1);

-- --------------------------------------------------------

--
-- Структура таблицы `equipment`
--

CREATE TABLE `equipment` (
  `equipment_id` int NOT NULL,
  `name` varchar(150) DEFAULT NULL,
  `image_url` text,
  `type_id` int DEFAULT NULL,
  `rental_price_per_day` decimal(10,2) DEFAULT NULL,
  `point_id` int DEFAULT NULL,
  `is_available` tinyint(1) DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `equipment`
--

INSERT INTO `equipment` (`equipment_id`, `name`, `image_url`, `type_id`, `rental_price_per_day`, `point_id`, `is_available`) VALUES
(1, 'Велосипед Trek X200', 'images/trek.jpg', 1, '500.00', 1, 1),
(2, 'Лыжи SnowFast', 'images/snow.jpg', 2, '600.00', 2, 1),
(3, 'Ролики SpeedRun', 'images/roll.jpg', 3, '350.00', 1, 1),
(4, 'Лыжи Atomic', 'images/atomic.jpg', 2, '750.00', 2, 0),
(5, 'Сноуборд Burton', 'images/burton.jpg', 4, '800.00', 3, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `equipment_types`
--

CREATE TABLE `equipment_types` (
  `type_id` int NOT NULL,
  `type_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `equipment_types`
--

INSERT INTO `equipment_types` (`type_id`, `type_name`) VALUES
(1, 'Велосипед'),
(2, 'Лыжи'),
(3, 'Ролики'),
(4, 'Сноуборд');

-- --------------------------------------------------------

--
-- Структура таблицы `pickup_points`
--

CREATE TABLE `pickup_points` (
  `point_id` int NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `pickup_points`
--

INSERT INTO `pickup_points` (`point_id`, `name`, `address`) VALUES
(1, 'Центральный', 'ул. Ленина, 15'),
(2, 'Северный', 'пр. Мира, 42'),
(3, 'Южный', 'ул. Гагарина, 8');

-- --------------------------------------------------------

--
-- Структура таблицы `rental_requests`
--

CREATE TABLE `rental_requests` (
  `request_id` int NOT NULL,
  `customer_id` int DEFAULT NULL,
  `equipment_id` int DEFAULT NULL,
  `employee_id` int DEFAULT NULL,
  `status_id` int DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `rental_requests`
--

INSERT INTO `rental_requests` (`request_id`, `customer_id`, `equipment_id`, `employee_id`, `status_id`, `start_date`, `end_date`, `created_at`) VALUES
(1, 1, 1, 1, 3, '2024-01-10', '2024-01-15', '2024-01-09 14:30:00'),
(2, 1, 3, 1, 4, '2024-01-05', '2024-01-07', '2024-01-04 10:15:00'),
(3, 2, 2, NULL, 1, '2024-01-15', '2024-01-20', '2024-01-14 16:45:00'),
(4, 2, 4, NULL, 2, '2024-01-20', '2024-01-25', '2024-01-18 09:20:00'),
(5, 3, 5, 2, 3, '2024-02-01', '2024-02-05', '2024-01-30 11:10:00');

-- --------------------------------------------------------

--
-- Структура таблицы `rental_statuses`
--

CREATE TABLE `rental_statuses` (
  `status_id` int NOT NULL,
  `status_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `rental_statuses`
--

INSERT INTO `rental_statuses` (`status_id`, `status_name`) VALUES
(1, 'Ожидание подтверждения'),
(2, 'Подтверждена'),
(3, 'Выдана'),
(4, 'Завершена'),
(5, 'Отменена');

-- --------------------------------------------------------

--
-- Структура таблицы `roles`
--

CREATE TABLE `roles` (
  `role_id` int NOT NULL,
  `role_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `roles`
--

INSERT INTO `roles` (`role_id`, `role_name`) VALUES
(1, 'Гость'),
(2, 'Клиент'),
(3, 'Сотрудник'),
(4, 'Администратор');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `user_id` int NOT NULL,
  `login` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `full_name` varchar(150) DEFAULT NULL,
  `role_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`user_id`, `login`, `password`, `full_name`, `role_id`) VALUES
(1, 'ivanov', 'pass123', 'Иван Иванов', 3),
(2, 'petrova', 'pass123', 'Мария Петрова', 2),
(3, 'sidorov', 'pass123', 'Петр Сидоров', 4);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Индексы таблицы `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`employee_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `point_id` (`point_id`);

--
-- Индексы таблицы `equipment`
--
ALTER TABLE `equipment`
  ADD PRIMARY KEY (`equipment_id`),
  ADD KEY `type_id` (`type_id`),
  ADD KEY `point_id` (`point_id`);

--
-- Индексы таблицы `equipment_types`
--
ALTER TABLE `equipment_types`
  ADD PRIMARY KEY (`type_id`);

--
-- Индексы таблицы `pickup_points`
--
ALTER TABLE `pickup_points`
  ADD PRIMARY KEY (`point_id`);

--
-- Индексы таблицы `rental_requests`
--
ALTER TABLE `rental_requests`
  ADD PRIMARY KEY (`request_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `equipment_id` (`equipment_id`),
  ADD KEY `employee_id` (`employee_id`),
  ADD KEY `status_id` (`status_id`);

--
-- Индексы таблицы `rental_statuses`
--
ALTER TABLE `rental_statuses`
  ADD PRIMARY KEY (`status_id`);

--
-- Индексы таблицы `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`role_id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `employees`
--
ALTER TABLE `employees`
  MODIFY `employee_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `equipment`
--
ALTER TABLE `equipment`
  MODIFY `equipment_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `equipment_types`
--
ALTER TABLE `equipment_types`
  MODIFY `type_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `pickup_points`
--
ALTER TABLE `pickup_points`
  MODIFY `point_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `rental_requests`
--
ALTER TABLE `rental_requests`
  MODIFY `request_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `rental_statuses`
--
ALTER TABLE `rental_statuses`
  MODIFY `status_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `roles`
--
ALTER TABLE `roles`
  MODIFY `role_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `customers`
--
ALTER TABLE `customers`
  ADD CONSTRAINT `customers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Ограничения внешнего ключа таблицы `employees`
--
ALTER TABLE `employees`
  ADD CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `employees_ibfk_2` FOREIGN KEY (`point_id`) REFERENCES `pickup_points` (`point_id`);

--
-- Ограничения внешнего ключа таблицы `equipment`
--
ALTER TABLE `equipment`
  ADD CONSTRAINT `equipment_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `equipment_types` (`type_id`),
  ADD CONSTRAINT `equipment_ibfk_2` FOREIGN KEY (`point_id`) REFERENCES `pickup_points` (`point_id`);

--
-- Ограничения внешнего ключа таблицы `rental_requests`
--
ALTER TABLE `rental_requests`
  ADD CONSTRAINT `rental_requests_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  ADD CONSTRAINT `rental_requests_ibfk_2` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`equipment_id`),
  ADD CONSTRAINT `rental_requests_ibfk_3` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`),
  ADD CONSTRAINT `rental_requests_ibfk_4` FOREIGN KEY (`status_id`) REFERENCES `rental_statuses` (`status_id`);

--
-- Ограничения внешнего ключа таблицы `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
