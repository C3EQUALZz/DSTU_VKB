using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using ThirdLaboratory.core.interfaces;

namespace ThirdLaboratory.models
{
    /// <summary>
    /// Модель, которая отвечает за второе задание. Модель в данном случае - это строки "Сотрудники" и "Заявки",
    /// взятые из ввода. 
    /// </summary>
    internal class SecondQuestionModel : ISecondQuestionModel
    {
        private string[] staffers;
        private string[] requests;

        /// <summary>
        /// Сеттер, который позволяет поставить сотрудников в классе
        /// </summary>
        /// <param name="value">1 строка из ввода в приложении</param>
        public void SetStaffers(string value)
        {
            staffers = Parse(value);
        }

        /// <summary>
        /// Сеттер, который позволяет поставить запросы в классе. 
        /// </summary>
        /// <param name="value">2 строка из ввода в приложении</param>
        public void SetRequests(string value)
        {
            requests = Parse(value); 
        }

        /// <summary>
        /// Точка запуска задания
        /// </summary>
        public string Execute()
        {

            if (requests.All(item => staffers.Contains(item)))
            {
                return "Все заявки содержат корректные фамилии";
            }

            var setOfStaffers = new HashSet<string>(staffers);
            var result = new StringBuilder("В массиве 'Сотрудники' нет таких: ");

            foreach (var staff in requests)
            {
                
                if (!(setOfStaffers.Contains(staff)))
                {
                    result.Append(staff + " ");
                }
            }

            return result.ToString();
        }

        /// <summary>
        /// Разделяем строку по ", " или "," или "," + пробел (n кол-во раз)
        /// </summary>
        /// <param name="value">строка из ввода, которую хотим распарсить в массив</param>
        /// <returns>массив строк, содержащий фамилии</returns>
        private string[] Parse(string value)
        {
            return Regex.Split(value, @",(\s+)?").Where(s => !string.IsNullOrWhiteSpace(s)).ToArray();
        }
    }
}
