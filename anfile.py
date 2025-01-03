class Group(models.Model):
   
    """Model to hold group details"""
   
    group_id = models.AutoField(_('group_id'), primary_key=True, db_index=True, help_text="Group ID")
    group_name = models.CharField(_('group_name'), max_length=255, help_text="Group name")
    location = models.CharField(_('location'), max_length=255, help_text="Location of the group")
    description = models.TextField(_('description'), max_length=2000, blank=True, help_text="Description of the group")
    admin = models.ManyToManyField(IgiUser, through='GroupAdminAssignment', related_name='admin_groups', help_text="Users who are admins of the group")
   
    class Meta:
        db_table = "group_details"
        verbose_name = _("Group")
   
    def __str__(self):
        return self.group_name
