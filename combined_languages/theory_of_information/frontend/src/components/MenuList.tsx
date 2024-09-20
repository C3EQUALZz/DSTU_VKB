import { Menu } from "antd"
import { BarsOutlined } from "@ant-design/icons"
import React from "react";
import { MenuListProps } from "../interfaces/MenuList";
import { Link } from "react-router-dom"

export const MenuList: React.FC<MenuListProps> = ({ darkTheme }) => {
    return (
        <Menu theme={darkTheme ? "dark" : "light"} mode="inline" className="menu-bar">
            <Menu.SubMenu key="fifth-semester-menu" icon={<BarsOutlined />} title="Пятый семестр">
                <Menu.Item key="fifth-sem-task-1">
                    <Link to="/">Лабораторная работа №1</Link>
                </Menu.Item>
                <Menu.Item key="fifth-sem-task-2">
                    <Link to="/5-sem/2-lab">Лабораторная работа №2</Link>
                </Menu.Item>
                <Menu.Item key="fifth-sem-task-3">
                    <Link to="/5-sem/3-lab">Лабораторная работа №3</Link>
                </Menu.Item>
                <Menu.Item key="fifth-sem-task-4">
                    <Link to="/5-sem/4-lab">Лабораторная работа №4</Link>
                </Menu.Item>
            </Menu.SubMenu>
            <Menu.SubMenu key="sixth-semester-menu" icon={<BarsOutlined />} title="Шестой семестр">
                <Menu.Item key="task-1">
                    <Link to="/6-sem/1-lab">Лабораторная работа №1</Link>
                </Menu.Item>
                <Menu.Item key="task-2">
                    <Link to="/6-sem/2-lab">Лабораторная работа №2</Link>
                </Menu.Item>
                <Menu.Item key="task-3">
                    <Link to="/6-sem/3-lab">Лабораторная работа №3</Link>
                </Menu.Item>
                <Menu.Item key="task-4">
                    <Link to="/6-sem/4-lab">Лабораторная работа №4</Link>
                </Menu.Item>
            </Menu.SubMenu>

        </Menu>
    )
}