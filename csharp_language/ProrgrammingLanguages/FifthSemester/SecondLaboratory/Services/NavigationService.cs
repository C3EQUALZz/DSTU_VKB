using SecondLaboratory.Structures;
using SecondLaboratory.Views.Calculator;
using SecondLaboratory.Enums;
using System.Windows.Forms;
using System.Collections.Generic;
using System;
using System.Linq;
using SecondLaboratory.Extensions;
using SecondLaboratory.Views.Converter.Converters;

namespace SecondLaboratory.Services;

public class NavigationService
{
    private Control NavigationContainer;
    private Control NavigationItemsContainer;
    private IList<NavigationItem> NavigationItems;

    private const int ITEMSPACING = 25;
    private const int GROUPSPACING = 40;
    private const int GROUPMARGINLEFT = 10;
    private const int ITEMMARGINLEFT = 15;

    public delegate void NavigatedHandler(NavigationItem item);
    public event NavigatedHandler Navigated;

    public NavigationService()
    {
        NavigationItems = new List<NavigationItem>();
    }

    public void Configure()
    {
        AddNavigation<StandartCalculatorForm>("Standart", CalculatorType.Calculator);
        AddNavigation<TimeConverterForm>("Time", CalculatorType.Converter);
    }

    public NavigationItem AddNavigation<T>(string title, CalculatorType calculatorType) where T : Form
    {
        var nav = new NavigationItem()
        {
            Title = title,
            FormType = typeof(T),
            CalculatorType = calculatorType
        };

        NavigationItems.Add(nav);

        return nav;
    }

    public NavigationItem Navigate<T>() where T : Form
    {
        return Navigate(NavigationItems.Where(x => x.FormType == typeof(T)).First());
    }

    private NavigationItem Navigate(NavigationItem item)
    {
        var form = (Form)Activator.CreateInstance(item.FormType);

        form.TopLevel = false;
        form.Dock = DockStyle.Fill;

        if (NavigationContainer.Controls.Count > 0) (NavigationContainer.Controls[0] as Form).Close();
        NavigationContainer.Controls.Clear();
        NavigationContainer.Controls.Add(form);

        form.Show();

        Navigated?.Invoke(item);

        return item;
    }

    public void AddNavigationControls()
    {
        var navigationGroups = GetNavigationGroups();

        var y = 0;

        foreach (var group in navigationGroups)
        {
            y += y == 0 ? 10 : GROUPSPACING;

            var label = new Label()
            {
                Text = group.Key.ToString(),
                Font = new System.Drawing.Font("Gadugi", 12, System.Drawing.FontStyle.Bold),
                Location = new System.Drawing.Point(GROUPMARGINLEFT, y)
            };

            NavigationItemsContainer.Controls.Add(label);

            foreach (var item in group.Value)
            {
                y += ITEMSPACING;

                var button = new Button()
                {
                    Text = item.Title,
                    Font = new System.Drawing.Font("Gadugi", 12),
                    Location = new System.Drawing.Point(ITEMMARGINLEFT, y),
                    FlatStyle = FlatStyle.Flat,
                    BackColor = System.Drawing.Color.Transparent,
                    Size = new System.Drawing.Size(200, 30),
                    TextAlign = System.Drawing.ContentAlignment.MiddleLeft
                };

                button.FlatAppearance.BorderSize = 0;
                button.FlatAppearance.MouseOverBackColor = System.Drawing.Color.FromArgb(50, 50, 50);
                button.FlatAppearance.MouseDownBackColor = System.Drawing.Color.FromArgb(50, 50, 50);
                button.SetRoundedShape(10);

                button.Click += (s, e) =>
                {
                    Navigate(item);
                };

                NavigationItemsContainer.Controls.Add(button);
            }
        }
    }

    private Dictionary<CalculatorType, List<NavigationItem>> GetNavigationGroups()
    {
        var groups = new Dictionary<CalculatorType, List<NavigationItem>>();

        foreach (var item in NavigationItems)
        {
            if (!groups.ContainsKey(item.CalculatorType))
            {
                groups.Add(item.CalculatorType, new List<NavigationItem>());
            }

            groups[item.CalculatorType].Add(item);
        }

        return groups;
    }

    public void SetNavigationContainer(Control control)
    {
        NavigationContainer = control;
    }

    public void SetNavigationItemsContainer(Control control)
    {
        NavigationItemsContainer = control;
    }
}
