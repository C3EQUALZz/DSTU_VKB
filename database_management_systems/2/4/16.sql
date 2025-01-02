/**
  Для каждого университета напишите запрос, выводящий количество работающих в нем преподавателей,
  с последующей сортировкой списка по этому количеству.
*/

SELECT
    COUNT("LECTURER_ID") as count_of_lectures,
    "UNIV_ID"
FROM "LECTURER"
GROUP BY "UNIV_ID"
ORDER BY count_of_lectures DESC