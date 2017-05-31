# ping.py

## Requirements

- MySQLdb

## Install dependencies with pip

`pip install -r requirements.txt`

## Mysql database schema
```sql
CREATE TABLE `ips` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` int(11) UNSIGNED NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ipId` int(11) NOT NULL,
  `ping1` float NOT NULL,
  `ping2` float NOT NULL,
  `ts` int(10) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(150) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `users_ips` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) NOT NULL,
  `ipId` int(11) NOT NULL,
  `description` text
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


ALTER TABLE `ips`
  ADD UNIQUE KEY `id` (`id`),
  ADD UNIQUE KEY `ip` (`ip`);

ALTER TABLE `logs`
  ADD UNIQUE KEY `id` (`id`),
  ADD KEY `ipId` (`ipId`),
  ADD KEY `ts` (`ts`);

ALTER TABLE `users`
  ADD UNIQUE KEY `id` (`id`),
  ADD UNIQUE KEY `login` (`login`);

ALTER TABLE `users_ips`
  ADD UNIQUE KEY `id` (`id`),
  ADD UNIQUE KEY `user_ip_uniq` (`userId`,`ipId`) USING BTREE;
```
