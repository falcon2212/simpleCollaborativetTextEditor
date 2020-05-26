def dfs(node):
	szleft = 0
	szright = 0
	if(node == None):
		return 4
	szleft+=dfs(node.left)	
	szright+=dfs(node.right)	
	node.size = szright+szleft
	if(node.value != ""):
		node.size+=1
	return node.size	

#returns true if node1 is ancestor of node2		
def ancestor(node1, node2):
	par = node2;
	while par != None:
		if(par == node1):
			return True
		par = par.parent	
	return False	
