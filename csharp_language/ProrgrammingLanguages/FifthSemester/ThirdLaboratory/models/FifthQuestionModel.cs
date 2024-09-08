using ThirdLaboratory.Core.Interfaces.FifthQuestion;

namespace ThirdLaboratory.Models
{
    internal class FifthQuestionModel : IFifthQuestionModel
    {
        /// <summary>
        /// Пример метода для валидации фамилии и имени
        /// </summary>
        public bool IsValidOwner(string owner)
        {
            var regex = new System.Text.RegularExpressions.Regex(@"^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?$");
            return regex.IsMatch(owner);
        }

        /// <summary>
        /// Пример метода для валидации номера машины (зависит от принятого формата)
        /// </summary>
        public bool IsValidCarNumber(string number)
        {
            var regex = new System.Text.RegularExpressions.Regex(@"^[А-Я]{1}\d{3}[А-Я]{2}$");
            return regex.IsMatch(number);
        }
    }
}
