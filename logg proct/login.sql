-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-05-2024 a las 03:17:02
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `login`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `articulos`
--

CREATE TABLE `articulos` (
  `id` int(11) NOT NULL,
  `descripcion` varchar(225) NOT NULL,
  `precio` decimal(65,2) NOT NULL,
  `itbis` decimal(65,2) NOT NULL,
  `cantidad` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `art_bill`
--

CREATE TABLE `art_bill` (
  `id` int(11) NOT NULL,
  `id_bills` int(11) NOT NULL,
  `decrition` varchar(255) NOT NULL,
  `price` decimal(65,2) NOT NULL,
  `itbis` decimal(65,2) NOT NULL,
  `amount` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `art_bill`
--

INSERT INTO `art_bill` (`id`, `id_bills`, `decrition`, `price`, `itbis`, `amount`) VALUES
(180, 1, 'pedro', 232.00, 40.00, 1),
(181, 1, 'teclado', 1222.00, 20.00, 1),
(182, 2, 'pedro', 232.00, 40.00, 1),
(183, 2, 'maus', 2222.00, 12.00, 1),
(184, 3, 'pedro', 232.00, 40.00, 1),
(185, 3, 'maus', 2222.00, 12.00, 1),
(186, 3, 'teclado', 3636.00, 3.00, 1),
(187, 4, 'pedro', 232.00, 40.00, 1),
(188, 4, 'maus', 2222.00, 12.00, 1),
(189, 4, 'teclado', 3636.00, 3.00, 1),
(190, 5, 'pedro', 232.00, 40.00, 1),
(191, 5, 'maus', 2222.00, 12.00, 1),
(192, 5, 'teclado', 3636.00, 3.00, 1),
(193, 6, 'pedro', 232.00, 40.00, 2),
(194, 6, 'juan', 100.00, 20.00, 3),
(195, 7, 'teclado', 3636.00, 3.00, 4),
(196, 7, 'juan', 100.00, 20.00, 1),
(197, 7, 'pedro', 22222.00, 1.00, 4),
(198, 8, 'maus', 2222.00, 12.00, 3),
(199, 9, 'maus', 2222.00, 12.00, 1),
(200, 1, 'teclado gamer 3g', 2256.00, 2.00, 3),
(201, 1, 'silla gamer tyron22', 5090.00, 2.00, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bills`
--

CREATE TABLE `bills` (
  `id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `number_bill` varchar(50) NOT NULL,
  `customer` varchar(255) NOT NULL,
  `discount` decimal(65,2) NOT NULL,
  `way_to_pay` varchar(255) NOT NULL,
  `paid` decimal(65,2) NOT NULL,
  `change` decimal(65,2) NOT NULL,
  `cashier` varchar(255) NOT NULL,
  `rnc_client_bill` int(11) NOT NULL,
  `ubicacion` varchar(255) NOT NULL,
  `contacto` varchar(255) NOT NULL,
  `total_general` decimal(65,2) NOT NULL,
  `estado` int(11) NOT NULL,
  `Itbisextra` decimal(65,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `bills`
--

INSERT INTO `bills` (`id`, `date`, `number_bill`, `customer`, `discount`, `way_to_pay`, `paid`, `change`, `cashier`, `rnc_client_bill`, `ubicacion`, `contacto`, `total_general`, `estado`, `Itbisextra`) VALUES
(1, '2024-05-02 12:21:32', '00001', 'hansel', 0.00, 'Efectivo', 368986.00, 351699.04, 'Hansel', 213453, 'Villa Maria', '12423456347', 17286.96, 1, 0.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clients`
--

CREATE TABLE `clients` (
  `client_id` int(11) NOT NULL,
  `client_name` varchar(50) NOT NULL,
  `client_address` varchar(50) NOT NULL,
  `client_phone` varchar(50) NOT NULL,
  `client_email` varchar(255) NOT NULL,
  `activity_id` int(11) NOT NULL,
  `rnc_client` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clients`
--

INSERT INTO `clients` (`client_id`, `client_name`, `client_address`, `client_phone`, `client_email`, `activity_id`, `rnc_client`) VALUES
(1, 'hansel', 'Villa Maria', '12423456347', 'slimerbatista27@gmail.com', 1, 213453),
(2, 'Carls', 'Ds Nacional 33', '1811333889', 'yucihansel@gmail.com', 2, 564),
(3, 'Luisa', 'Palacio de los caballeros', '18495856654', 'xLekhansel@hotmail.com', 3, 898);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario`
--

CREATE TABLE `inventario` (
  `id` int(11) NOT NULL,
  `descripcion` varchar(225) NOT NULL,
  `precio` decimal(57,2) NOT NULL,
  `cantidad` bigint(20) NOT NULL,
  `itbis` decimal(65,2) NOT NULL,
  `img` varchar(255) NOT NULL,
  `cantidad_a` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventario`
--

INSERT INTO `inventario` (`id`, `descripcion`, `precio`, `cantidad`, `itbis`, `img`, `cantidad_a`) VALUES
(9, 'teclado gamer 3g', 2256.00, 53, 2.00, 'tacladogamer1.avif', 0),
(10, 'teclado gamer turb45', 3445.00, 66, 0.00, 'tecladgamer2.jpg', 66),
(11, 'silla gamer tyron22', 5090.00, 76, 2.00, 'Silla-Gaming.jpg', 0),
(12, 'silla tyop', 5456.00, 99, 2.00, 'sillagamer2.jpg', 99),
(13, 'silla 334', 5556.00, 88, 1.00, 'sillagamer1.jpg', 88),
(14, 'Logitech g203', 2334.00, 899, 4.00, 'mausgamer1.jpg', 899),
(15, 'estelar 433', 2334.00, 99, 3.00, 'mausgamer2.jpg', 99),
(16, 'teclado gamerff', 5543457.00, 233, 54.00, 'sey-removebg-preview.png', 233);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `description` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `description`) VALUES
(1, 'admin'),
(2, 'usuario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `id_rol` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `correo`, `password`, `id_rol`) VALUES
(1, 'usario1@gmail.com', '123', 1),
(8, 'papa@gmail.com', '123', 2),
(9, 'user@gmail.com', '111', 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `articulos`
--
ALTER TABLE `articulos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `art_bill`
--
ALTER TABLE `art_bill`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_bills` (`id_bills`);

--
-- Indices de la tabla `bills`
--
ALTER TABLE `bills`
  ADD PRIMARY KEY (`id`),
  ADD KEY `estado` (`estado`);

--
-- Indices de la tabla `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`client_id`),
  ADD KEY `activity_id` (`activity_id`);

--
-- Indices de la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `articulos`
--
ALTER TABLE `articulos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `art_bill`
--
ALTER TABLE `art_bill`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=202;

--
-- AUTO_INCREMENT de la tabla `bills`
--
ALTER TABLE `bills`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `clients`
--
ALTER TABLE `clients`
  MODIFY `client_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `inventario`
--
ALTER TABLE `inventario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
