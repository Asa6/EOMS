from django.utils.safestring import mark_safe

class Paging:
    def __init__(self, current_page, all_count, page_count=20, pager_num=5):
        """
        :current_page 当前点击的页号:
        :all_count 数据总条数:
        :page_count 每页显示的条数:
        :pager_num 页码个数:
        """
        self.current_page = current_page
        self.page_count = page_count
        self.pager_num = pager_num
        self.all_count = all_count
        self.page_list = []

    @property
    def start(self):
        return (self.current_page - 1) * self.page_count

    @property
    def end(self):
        return self.current_page * self.page_count

    @property
    def total_count(self):
        t, m = divmod(self.all_count, self.page_count)
        if m:
            t += 1
        return t

    def page_str(self, url):
        if self.total_count < self.pager_num:
            self.start_index = 1
            self.end_index = self.total_count + 1
        else:
            if self.current_page <= (self.pager_num + 1)/2:
                self.start_index = 1
                self.end_index = self.pager_num + 1
            else:
                self.start_index = self.current_page - (self.pager_num - 1)/2
                self.end_index = self.current_page + (self.pager_num + 1)/2
                if (self.current_page + (self.pager_num - 1)/2) > self.total_count:
                    self.end_index = self.total_count + 1
                    self.start_index = self.total_count - self.pager_num + 1


        if self.current_page <= 1:
            last_page = '<li class="disabled"><a href="javascript:void(0)">&laquo;</a></li>'
            self.page_list.append(last_page)
        else:
            last_page = '<li><a href="%s?page_number=%s">&laquo;</a></li>' % (url, self.current_page - 1)
            self.page_list.append(last_page)

        for i in range(int(self.start_index), int(self.end_index)):
            if i == self.current_page:
                temp = '<li class="active"><a href="javascript:void(0)">%s</a></li>\n' % (i)
            else:
                temp = '<li><a href="%s?page_number=%s">%s</a></li>\n' % (url, i, i)

            self.page_list.append(temp)

        if self.current_page >= self.total_count:
            next_page = '<li class="disabled"><a href="javascript:void(0)">&raquo;</a></li>'
            self.page_list.append(next_page)
        else:
            next_page = '<li><a href="%s?page_number=%s">&raquo;</a></li>' % (url, self.current_page + 1)
            self.page_list.append(next_page)

        return mark_safe("".join(self.page_list))