using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using ThirdLaboratory.Core.Interfaces.SixthQuestion;

namespace ThirdLaboratory.Models
{
    internal class SixthQuestionModel : ISixthQuestionModel
    {

        public string Execute(string scholarShips, string scholarShipRange, string students)
        {

            var numbers = Regex.Split(scholarShipRange, @"\s*-\s*").Select(x => Convert.ToInt32(x)).ToArray();
            var (first, second) = (numbers[0], numbers[1]);

            var scholarShipNumbers = Regex.Split(scholarShips, @"\s*,\s*").Select(x => Convert.ToInt32(x));

            if (!scholarShipNumbers.All(number => number >= first && number <= second))
            {
                return "Не все стипендии входят в нужный диапазон";
            }

            return Regex.Split(students, @"\s*,\s*").Zip(scholarShipNumbers, (scholarship, student) => (scholarship, student)).ToString();
        }
    }
}
