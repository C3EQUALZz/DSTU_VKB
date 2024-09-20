import React from "react";
import { Button } from "antd"
import {HiOutlineSun, HiOutlineMoon} from "react-icons/hi";
import { ToggleThemeButtonProps } from "../interfaces/ToggleThemeButton";

const ToggleThemeButton: React.FC<ToggleThemeButtonProps> = ({darkTheme, toggleTheme}) => {
    return (
        <div className="toggle-theme-button">
            <Button onClick={toggleTheme}>
                {darkTheme ? <HiOutlineSun /> : <HiOutlineMoon />}
            </Button>
        </div>
    )
}

export default ToggleThemeButton;