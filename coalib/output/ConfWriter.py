"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
from coalib.settings.Settings import Settings


class ConfWriter:
    def __init__(self,
                 file_name,
                 key_value_delimiter='=',
                 comment_seperators=['#', ';', '//'],
                 key_delimiter=',',
                 section_name_surrounding_beg='[',
                 section_name_surrounding_end="]"):
        self.__file_name = file_name
        self.__file = open(self.__file_name, "w")
        self.__key_value_delimiter = key_value_delimiter
        self.__comment_seperators = comment_seperators
        self.__key_delimiter = key_delimiter
        self.__section_name_surrounding_beg = section_name_surrounding_beg
        self.__section_name_surrounding_end = section_name_surrounding_end

    def __del__(self):
        self.__file.close()

    def write_sections(self, sections):
        for section in sections:
            self.write_section(sections[section])

    def write_section(self, section):
        if not isinstance(section, Settings):
            raise TypeError

        self.__write_section_name(section.name)

        keys = []
        val = None
        # Fixme: I dont think I handle the iterators the right way here
        it = section.__iter__(ignore_defaults=True)
        try:
            while True:
                setting = section[it.__next__()]
                if str(setting) == val:
                    keys.append(setting.key)
                else:
                    self.__write_key_val(keys, val)
                    keys = [setting.key]
                    val = str(setting)
        except StopIteration:
            self.__write_key_val(keys, val)

    def __write_section_name(self, name):
        self.__file.write(self.__section_name_surrounding_beg + name +
                          self.__section_name_surrounding_end + '\n')

    def __write_key_val(self, keys, val):
        if keys == []:
            return

        for sep in self.__comment_seperators:
            if val[0:len(sep)] == sep:
                self.__file.write(val + "\n")
                return

        delim = ""
        for key in keys:
            self.__file.write(delim + key)
            if delim == "":
                delim = self.__key_delimiter + " "

        self.__file.write(" " + self.__key_value_delimiter + " " + val + "\n")