import { Menu } from "antd"
import { BarsOutlined } from "@ant-design/icons"
import React from "react";
import { MenuListProps } from "../interfaces/MenuList";

export const MenuList: React.FC<MenuListProps> = ({ darkTheme }) => {
    return (
        <Menu theme={darkTheme ? "dark" : "light"} mode="inline" className="menu-bar">
            <Menu.SubMenu key="fifth-semester-menu" icon={<BarsOutlined />} title="Пятый семестр">
                <Menu.Item key="task-1">
                    Лабораторная работа №1
                </Menu.Item>
                <Menu.Item key="task-2">
                    Лабораторная работа №2
                </Menu.Item>
                <Menu.Item key="task-3">
                    Лабораторная работа №3
                </Menu.Item>
                <Menu.Item key="task-4">
                    Лабораторная работа №4
                </Menu.Item>
            </Menu.SubMenu>
            <Menu.SubMenu key="sixth-semester-menu" icon={<BarsOutlined />} title="Шестой семестр">
                <Menu.Item key="task-1">
                    Лабораторная работа №1
                </Menu.Item>
                <Menu.Item key="task-2">
                    Лабораторная работа №2
                </Menu.Item>
                <Menu.Item key="task-3">
                    Лабораторная работа №3
                </Menu.Item>
                <Menu.Item key="task-4">
                    Лабораторная работа №4
                </Menu.Item>
            </Menu.SubMenu>

        </Menu>
    )
}