/**
 * Данный интерфейс нужен для связки элементов. Делается с той целью, чтобы был полиморфизм у UI элементов.
 */
package programmingLanguagesJava.laboratories.GUI.controllers.laboratories;

interface ElementLaboratory {
    /**
     * Запуск обработки элемента UI
     */
    void event();
}
