class Checkbox:
    def __init__(self, surface, x, y, idnum, pygame, color=(230, 230, 230),
        caption="", outline_color=(0, 0, 0), check_color=(0, 0, 0),
        font_size=22, font_color=(0, 0, 0),
    text_offset=(28, 1), font='Ariel Black'):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.ft = font
        self.pygame = pygame

        #identification for removal and reorginazation
        self.idnum = idnum

        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 12, 12)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = False

    def _draw_button_text(self):
        self.font = self.pygame.font.SysFont(self.ft, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + 12 / 2 - h / 2 +
        self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            self.pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            self.pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            self.pygame.draw.circle(self.surface, self.cc, (self.x + 6, self.y + 6), 4)

        elif not self.checked:
            self.pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            self.pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self, grid, checkboxes, location):
        x, y = location
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.idnum < 3 and grid.current_searchAlgorithm != self.idnum:
                self.checked = True
                checkboxes[grid.current_searchAlgorithm].checked = False
                grid.current_searchAlgorithm = self.idnum
            elif self.idnum > 2 and self.idnum < 5:
                self.checked = not self.checked
                if self.checked:
                    grid.current_AnimationSettings.append(self.idnum)
                else:
                    grid.current_AnimationSettings.remove(self.idnum)
            elif self.idnum >= 5 and grid.current_genMaze != self.idnum:
                self.checked = True
                checkboxes[grid.current_genMaze].checked = False
                grid.current_genMaze = self.idnum

