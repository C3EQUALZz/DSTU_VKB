import { Menu } from "antd";
import { BarsOutlined } from "@ant-design/icons";
import React from "react";
import { MenuListProps } from "../interfaces/MenuList";
import { Link } from "react-router-dom";

export const MenuList: React.FC<MenuListProps> = ({ darkTheme }) => {
    const items = [
        {
            label: 'Пятый семестр',
            key: 'fifth-semester-menu',
            icon: <BarsOutlined />,
            children: [
                {
                    label: <Link to="/">Лабораторная работа №1</Link>,
                    key: 'fifth-sem-task-1',
                },
                {
                    label: <Link to="/5-sem/2-lab">Лабораторная работа №2</Link>,
                    key: 'fifth-sem-task-2',
                },
                {
                    label: <Link to="/5-sem/3-lab">Лабораторная работа №3</Link>,
                    key: 'fifth-sem-task-3',
                },
                {
                    label: <Link to="/5-sem/4-lab">Лабораторная работа №4</Link>,
                    key: 'fifth-sem-task-4',
                },
            ],
        },
        {
            label: 'Шестой семестр',
            key: 'sixth-semester-menu',
            icon: <BarsOutlined />,
            children: [
                {
                    label: <Link to="/6-sem/1-lab">Лабораторная работа №1</Link>,
                    key: 'task-1',
                },
                {
                    label: <Link to="/6-sem/2-lab">Лабораторная работа №2</Link>,
                    key: 'task-2',
                },
                {
                    label: <Link to="/6-sem/3-lab">Лабораторная работа №3</Link>,
                    key: 'task-3',
                },
                {
                    label: <Link to="/6-sem/4-lab">Лабораторная работа №4</Link>,
                    key: 'task-4',
                },
            ],
        },
    ];

    return (
        <Menu theme={darkTheme ? "dark" : "light"} mode="inline" className="menu-bar" items={items} />
    );
};
