-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 19-Fev-2024 às 12:31
-- Versão do servidor: 10.4.27-MariaDB
-- versão do PHP: 8.0.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `prisebot`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `application_area`
--

CREATE TABLE `application_area` (
  `id` int(11) NOT NULL,
  `description` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `application_area`
--

INSERT INTO `application_area` (`id`, `description`) VALUES
(1, 'Aspects'),
(2, 'Adaptative System');

-- --------------------------------------------------------

--
-- Estrutura da tabela `constructrs`
--

CREATE TABLE `constructrs` (
  `id` int(11) NOT NULL,
  `id_extension` int(11) DEFAULT NULL,
  `title_en` varchar(250) NOT NULL,
  `title_pt` varchar(250) NOT NULL,
  `concept_pt` varchar(250) DEFAULT NULL,
  `concept_en` varchar(250) DEFAULT NULL,
  `image` varchar(250) DEFAULT NULL,
  `description_pt` text DEFAULT NULL,
  `description_en` text DEFAULT NULL,
  `form_pt` varchar(250) DEFAULT NULL,
  `form_en` varchar(250) DEFAULT NULL,
  `classification_pt` varchar(250) DEFAULT NULL,
  `classification_en` varchar(250) DEFAULT NULL,
  `notation` varchar(250) DEFAULT NULL,
  `example` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `constructrs`
--

INSERT INTO `constructrs` (`id`, `id_extension`, `title_en`, `title_pt`, `concept_pt`, `concept_en`, `image`, `description_pt`, `description_en`, `form_pt`, `form_en`, `classification_pt`, `classification_en`, `notation`, `example`) VALUES
(1, 1, 'Cardinality Means-End Link', 'Link Meio-Fim da Cardinalidade', 'Link Meio-Fim da Cardinalidade', 'Cardinality Means-End Link', 'Cardinalidade Ligação meio-fim', 'Adição de cardinalidade em ligações de meios-fim', 'Addition of cardinality in means-end links', 'seta', 'arrow', NULL, NULL, 'https://istarextensions.cin.ufpe.br/catalogue/images/1479031468.jpg', 'https://istarextensions.cin.ufpe.br/catalogue/images/1479031468b.jpg'),
(2, 2, 'Failure', 'Falha', 'Falha, erro, defeito', 'Failure, error, fail', 'https://istarextensions.cin.ufpe.br/catalogue/images/1478980783.jpg', 'Esta construtor é utilizada para representar as falhas do sistema auto-adaptativo', 'This construct is used to represent Self-adaptive system failures', 'salpicos', 'splash', NULL, NULL, 'https://istarextensions.cin.ufpe.br/catalogue/images/1478980783.jpg', 'https://istarextensions.cin.ufpe.br/catalogue/images/1478980783b.jpg');

-- --------------------------------------------------------

--
-- Estrutura da tabela `extensions`
--

CREATE TABLE `extensions` (
  `id` int(11) NOT NULL,
  `title_en` text DEFAULT NULL,
  `title_pt` varchar(250) NOT NULL,
  `authors` text DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `source` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `extensions`
--

INSERT INTO `extensions` (`id`, `title_en`, `title_pt`, `authors`, `year`, `source`) VALUES
(1, 'A comparison of goal-oriented approaches to model software product lines variability', '', 'Borba, Clarissa; Silva, Carla', 2009, 'International Conference on Conceptual Modeling'),
(2, 'Engineering requirements for adaptive systems', 'Requisitos de engenharia para sistemas adaptativos', 'Morandini, Mirko; Penserini, Loris; Perini, Anna; Marchetto, Alessandro', 2015, 'Requirements Engineering Journal');

-- --------------------------------------------------------

--
-- Estrutura da tabela `extension_area`
--

CREATE TABLE `extension_area` (
  `id` int(11) NOT NULL,
  `id_extension` int(11) NOT NULL,
  `id_area` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `extension_area`
--

INSERT INTO `extension_area` (`id`, `id_extension`, `id_area`) VALUES
(1, 1, 1),
(2, 2, 2);

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `application_area`
--
ALTER TABLE `application_area`
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `constructrs`
--
ALTER TABLE `constructrs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_extension` (`id_extension`);

--
-- Índices para tabela `extensions`
--
ALTER TABLE `extensions`
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `extension_area`
--
ALTER TABLE `extension_area`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_extension` (`id_extension`),
  ADD KEY `id_area` (`id_area`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `application_area`
--
ALTER TABLE `application_area`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `constructrs`
--
ALTER TABLE `constructrs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `extensions`
--
ALTER TABLE `extensions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `extension_area`
--
ALTER TABLE `extension_area`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `constructrs`
--
ALTER TABLE `constructrs`
  ADD CONSTRAINT `constructrs_ibfk_1` FOREIGN KEY (`id_extension`) REFERENCES `extensions` (`id`);

--
-- Limitadores para a tabela `extension_area`
--
ALTER TABLE `extension_area`
  ADD CONSTRAINT `extension_area_ibfk_1` FOREIGN KEY (`id_extension`) REFERENCES `extensions` (`id`),
  ADD CONSTRAINT `extension_area_ibfk_2` FOREIGN KEY (`id_area`) REFERENCES `application_area` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
