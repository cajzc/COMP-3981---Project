function TrimList(list, limit){
	for(var i = ds_list_size(list) - 1; i > limit - 1; i--) {
			ds_list_delete(list, i);
		}
}