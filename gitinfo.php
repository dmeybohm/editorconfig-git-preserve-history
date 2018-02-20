#!/usr/bin/env php
<?php

$commitlog = $_SERVER['argv'][1];
if (preg_match('/^commit (\S+)$/m', $commitlog, $matches)) {
	$commit = $matches[1];
}
if (preg_match('/^Author: (.*)$/m', $commitlog, $matches)) {
	$author = $matches[1];
}
if (preg_match('/^Date: \s*(.*)$/m', $commitlog, $matches)) {
	$date = $matches[1];
}
$message = preg_replace('/^(.*)\n\n/ms', '', $commitlog);
$message = preg_replace('/^\s{4}/m', '', $message);

echo $commit, "\n", $author, "\n", $date, "\n", $message;

